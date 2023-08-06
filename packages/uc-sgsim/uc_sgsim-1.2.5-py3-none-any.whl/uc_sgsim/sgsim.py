import time
import sys
from pathlib import Path
from typing import Union
from ctypes import CDLL, POINTER, c_double, c_int
from multiprocessing import Pool

import numpy as np
from uc_sgsim.kriging import Kriging
from uc_sgsim.random_field import SgsimField
from uc_sgsim.cov_model.base import CovModel
from uc_sgsim.utils import CovModelStructure, SgsimStructure

BASE_DIR = Path(__file__).resolve().parent


class UCSgsim(SgsimField):
    def __init__(
        self,
        x: int,
        model: CovModel,
        realization_number: int,
        kriging: Union[str, Kriging] = 'SimpleKriging',
        **kwargs,
    ):
        super().__init__(x, model, realization_number, kriging, **kwargs)

    def _process(self, randomseed: int = 0, parallel: bool = False) -> np.array:
        self.randomseed = randomseed
        if parallel is False:
            self.n_process = 1

        counts = 0

        start_time = time.time()
        np.random.seed(self.randomseed)
        while counts < (self.realization_number // self.n_process):
            drop = False
            unsampled = np.linspace(1, self.x_size - 2, self.x_size - 2)
            y_value = np.random.normal(0, self.model.sill**0.5, 2).reshape(2, 1)
            x_grid = np.array([0, self.x_size - 1]).reshape(2, 1)
            z = np.zeros(self.x_size)
            z[0], z[-1] = y_value[0], y_value[1]
            neigh = 0

            grid = np.hstack([x_grid, y_value])

            randompath = np.random.choice(
                unsampled,
                len(unsampled),
                replace=False,
            )

            for i in range(len(unsampled)):
                z[int(randompath[i])] = self.kriging.simulation(
                    grid,
                    randompath[i],
                    neighbor=neigh,
                )
                if z[int(randompath[i])] >= self.z_max or z[int(randompath[i])] <= self.z_min:
                    drop = True
                    break
                temp = np.hstack([randompath[i], z[int(randompath[i])]])
                grid = np.vstack([grid, temp])

                if neigh < self.max_neigh:
                    neigh += 1

            self.randomseed += 1
            if drop is False:
                self.random_field[counts, :] = z
                counts = counts + 1
            print('Progress = %.2f' % (counts / self.realization_number * 100) + '%', end='\r')

        print('Progress = %.2f' % 100 + '%\n', end='\r')
        end_time = time.time()
        print('Time = %f' % (end_time - start_time), 's\n')

        return self.random_field

    def compute(self, n_process: int, randomseed: int) -> np.array:
        pool = Pool(processes=n_process)
        self.n_process = n_process
        self.realization_number = self.realization_number * n_process
        self.random_field = np.empty([self.realization_number, self.x_size])

        rand_list = [randomseed + i for i in range(n_process)]
        parallel = [True] * n_process

        z = pool.starmap(self._process, zip(rand_list, parallel))
        pool.close()
        # use pool.join() to measure the coverage of sub process
        pool.join()

        for i in range(n_process):
            start = int(i * self.realization_number / n_process)
            end = int((i + 1) * self.realization_number / n_process)
            self.random_field[start:end, :] = z[i][: end - start, :]

        return self.random_field

    def variogram_compute(self, n_process: int = 1) -> None:
        pool = Pool(processes=n_process)
        model_len = self.x_size
        x = np.linspace(0, self.x_size - 1, model_len).reshape(model_len, 1)

        grid = [
            np.hstack([x, self.random_field[i, :].reshape(model_len, 1)])
            for i in range(self.realization_number)
        ]
        self.variogram = pool.starmap(self.model.variogram, zip(grid))
        pool.close()
        # use pool.join() to measure the coverage of sub process
        pool.join()
        self.variogram = np.array(self.variogram)


class UCSgsimDLL(UCSgsim):
    def __init__(
        self,
        x: int,
        model: CovModel,
        realization_number: int,
        kriging: str = 'SimpleKriging',
        **kwargs,
    ):
        super().__init__(x, model, realization_number, **kwargs)
        self.kriging = kriging

    def _lib_read(self) -> CDLL:
        if sys.platform.startswith('linux'):
            lib = CDLL(str(BASE_DIR) + r'/c_core/uc_sgsim.so')
        elif sys.platform.startswith('win32'):
            lib = CDLL(str(BASE_DIR) + r'/c_core/uc_sgsim.dll', winmode=0)
        return lib

    def _cpdll(self, randomseed: int) -> np.array:
        lib = self._lib_read()
        mlen = int(self.x_size)
        realization_number = int(self.realization_number // self.n_process)
        random_field = np.empty([realization_number, self.x_size])

        kriging = 1 if self.kriging == 'OrdinaryKriging' else 0
        sgsim_s = SgsimStructure(
            x_len=mlen,
            realization_numbers=realization_number,
            randomseed=randomseed,
            kirging_method=kriging,
            if_alloc_memory=0,
            array=(c_double * (mlen * realization_number))(),
            z_min=self.z_min,
            z_max=self.z_max,
        )

        cov_s = CovModelStructure(
            bw_l=self.model.bandwidth_len,
            bw_s=self.model.bandwidth_step,
            bw=self.model.bandwidth_len // self.model.bandwidth_step,
            max_neighbor=self.max_neigh,
            range=self.model.k_range,
            sill=self.model.sill,
            nugget=self.model.nugget,
        )

        sgsim = lib.sgsim_run
        sgsim.argtypes = (POINTER(SgsimStructure), POINTER(CovModelStructure), c_int)
        sgsim(sgsim_s, cov_s, 0)

        for i in range(realization_number):
            random_field[i, :] = sgsim_s.array[i * mlen : (i + 1) * mlen]
        return random_field

    def compute(self, n_process: int, randomseed: int) -> np.array:
        pool = Pool(processes=n_process)
        self.n_process = n_process

        if n_process > 1:
            self.realization_number = self.realization_number * n_process

        self.random_field = np.empty([self.realization_number, self.x_size])

        rand_list = [randomseed + i for i in range(n_process)]

        z = pool.starmap(self._cpdll, zip(rand_list))

        pool.close()
        # use pool.join() to measure the coverage of sub process
        pool.join()

        for i in range(n_process):
            start = int(i * self.realization_number / n_process)
            end = int((i + 1) * self.realization_number / n_process)
            self.random_field[start:end, :] = z[i][: end - start, :]

        return self.random_field

    def _variogram_cpdll(self, n_process: int) -> np.array:
        lib = self._lib_read()
        vario = lib.variogram
        vario.argtypes = (
            POINTER(c_double),
            POINTER(c_double),
            c_int,
            c_int,
            c_int,
        )
        vario.restype = None

        mlen = int(self.x_size)
        realization_number = int(self.realization_number // self.n_process)

        vario_size = len(self.bandwidth)

        vario_array = (c_double * (vario_size))()
        random_field_array = (c_double * (mlen))()

        variogram = np.empty([realization_number, vario_size])

        for i in range(realization_number):
            random_field_array[:] = self.random_field[i + n_process * realization_number, :]
            vario(random_field_array, vario_array, mlen, vario_size, 1)
            variogram[i, :] = list(vario_array)

        return variogram

    def variogram_compute(self, n_process: int = 1) -> np.array:
        pool = Pool(processes=n_process)
        self.n_process = n_process

        self.variogram = np.empty([self.realization_number, len(self.bandwidth)])
        cpu_number = [i for i in range(self.n_process)]

        z = pool.starmap(self._variogram_cpdll, zip(cpu_number))
        pool.close()
        # use pool.join() to measure the coverage of sub process
        pool.join()

        for i in range(n_process):
            for j in range(int(self.realization_number / n_process)):
                self.variogram[(j + int(i * self.realization_number / n_process)), :] = z[i][j, :]
        return self.variogram
