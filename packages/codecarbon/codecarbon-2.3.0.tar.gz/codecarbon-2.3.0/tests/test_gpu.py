# -*- coding: utf-8 -*-

# Copyright (C) 2020 [COMET-ML]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import os.path
import sys
from copy import copy, deepcopy
from unittest import mock

import pynvml as real_pynvml


class FakeGPUEnv:
    def setup_method(self):
        self.old_sys_path = copy(sys.path)
        fake_module_path = os.path.join(os.path.dirname(__file__), "fake_modules")
        sys.path.insert(0, fake_module_path)

        # Clean old modules
        try:
            del sys.modules["pynvml"]
        except KeyError:
            pass

        try:
            del sys.modules["codecarbon.core.gpu"]
        except KeyError:
            pass

        # Setup the state, strings are returned as bytes
        self.DETAILS = {
            "handle_0": {
                "name": b"GeForce GTX 1080",
                "uuid": b"uuid#1",
                "memory": real_pynvml.c_nvmlMemory_t(1024, 100, 924),
                "temperature": 75,
                "power_usage": 26,
                "total_energy_consumption": 1000,
                "power_limit": 149,
                "utilization_rate": real_pynvml.c_nvmlUtilization_t(96, 0),
                "compute_mode": 0,
                "compute_processes": [
                    real_pynvml.c_nvmlProcessInfo_t(16, 1024 * 1024),
                    real_pynvml.c_nvmlProcessInfo_t(32, 2 * 1024 * 1024),
                ],
                "graphics_processes": [],
            },
            "handle_1": {
                "name": b"GeForce GTX 1080",
                "uuid": b"uuid#2",
                "memory": real_pynvml.c_nvmlMemory_t(1024, 200, 824),
                "temperature": 79,
                "power_usage": 29,
                "total_energy_consumption": 800,
                "power_limit": 149,
                "utilization_rate": real_pynvml.c_nvmlUtilization_t(0, 100),
                "compute_mode": 2,
                "compute_processes": [],
                "graphics_processes": [
                    real_pynvml.c_nvmlProcessInfo_t(8, 1024 * 1024 * 1024),
                    real_pynvml.c_nvmlProcessInfo_t(64, 2 * 1024 * 1024 * 1024),
                ],
            },
        }
        self.expected = [
            {
                "name": "GeForce GTX 1080",
                "uuid": "uuid#1",
                "total_memory": 1024,
                "free_memory": 100,
                "used_memory": 924,
                "temperature": 75,
                "power_usage": 26,
                "power_limit": 149,
                "total_energy_consumption": 1000,
                "gpu_utilization": 96,
                "compute_mode": 0,
                "compute_processes": [
                    {"pid": 16, "used_memory": 1024 * 1024},
                    {"pid": 32, "used_memory": 2 * 1024 * 1024},
                ],
                "graphics_processes": [],
            },
            {
                "name": "GeForce GTX 1080",
                "uuid": "uuid#2",
                "total_memory": 1024,
                "free_memory": 200,
                "used_memory": 824,
                "temperature": 79,
                "power_usage": 29,
                "power_limit": 149,
                "total_energy_consumption": 800,
                "gpu_utilization": 0,
                "compute_mode": 2,
                "compute_processes": [],
                "graphics_processes": [
                    {"pid": 8, "used_memory": 1024 * 1024 * 1024},
                    {"pid": 64, "used_memory": 2 * 1024 * 1024 * 1024},
                ],
            },
        ]
        import pynvml

        pynvml.DETAILS = self.DETAILS
        pynvml.INIT_MOCK.reset_mock()

    def teardown_method(self):
        # Restore the old paths
        sys.path = self.old_sys_path
        try:
            del sys.modules["codecarbon.external.hardware"]
        except KeyError:
            pass


class TestGpu(FakeGPUEnv):
    def test_is_gpu_details_available(self):
        from codecarbon.core.gpu import is_gpu_details_available

        assert is_gpu_details_available() is True

    def test_static_gpu_info(self):
        from codecarbon.core.gpu import AllGPUDevices

        alldevices = AllGPUDevices()
        expected = [
            {
                "name": "GeForce GTX 1080",
                "uuid": "uuid#1",
                "total_memory": 1024,
                "power_limit": 149,
                "gpu_index": 0,
            },
            {
                "name": "GeForce GTX 1080",
                "uuid": "uuid#2",
                "total_memory": 1024,
                "power_limit": 149,
                "gpu_index": 1,
            },
        ]

        assert alldevices.get_gpu_static_info() == expected

    def test_gpu_details(self):
        from codecarbon.core.gpu import AllGPUDevices

        alldevices = AllGPUDevices()

        assert alldevices.get_gpu_details() == self.expected

    def test_gpu_no_power_limit(self):
        import pynvml

        from codecarbon.core.gpu import AllGPUDevices

        def raiseException(handle):
            raise Exception("Some bad exception")

        pynvml.nvmlDeviceGetEnforcedPowerLimit = raiseException
        alldevices = AllGPUDevices()

        expected_power_limit = deepcopy(self.expected)
        expected_power_limit[0]["power_limit"] = None
        expected_power_limit[1]["power_limit"] = None

        assert alldevices.get_gpu_details() == expected_power_limit

    def test_gpu_metadata_total_power(self):
        """
        Get the total power of all GPUs
        """
        # Prepare
        # (Note: This imports should be inside the test, not on top of the file, otherwise the mock does not work)
        from codecarbon.core.units import Energy, Power, Time
        from codecarbon.external.hardware import GPU

        gpu1_energy1 = Energy.from_millijoules(149701)
        gpu1_energy2 = Energy.from_millijoules(180000)
        gpu2_energy1 = Energy.from_millijoules(149702)
        gpu2_energy2 = Energy.from_millijoules(180000)

        gpu2_power = Power.from_energies_and_delay(gpu1_energy1, gpu1_energy2, Time(5))
        gpu1_power = Power.from_energies_and_delay(gpu2_energy1, gpu2_energy2, Time(5))
        expected_power = gpu1_power + gpu2_power

        # Call
        with mock.patch(
            "pynvml.nvmlDeviceGetTotalEnergyConsumption",
            side_effect=[149701, 149702, 180000, 180000],  # Mock the energy consumption
        ):
            gpu = GPU.from_utils()
            gpu.measure_power_and_energy(5)

        # Assert
        assert expected_power.kW == gpu.total_power().kW

    def test_gpu_metadata_one_gpu_power(self):
        """
        Get the power of just one GPU even if there are more than 1
        """
        # Prepare
        # (Note: This imports should be inside the test, not on top of the file, otherwise the mock does not work)
        from codecarbon.core.units import Energy, Power, Time
        from codecarbon.external.hardware import GPU

        # Call
        with mock.patch(
            "pynvml.nvmlDeviceGetTotalEnergyConsumption",
            side_effect=[149701, 149702, 180000, 180000],  # Mock the energy consumption
        ):
            gpu = GPU.from_utils()
            gpu.measure_power_and_energy(5, gpu_ids=[1])

        # Assert
        gpu2_energy1 = Energy.from_millijoules(149702)
        gpu2_energy2 = Energy.from_millijoules(180000)

        gpu2_power = Power.from_energies_and_delay(gpu2_energy1, gpu2_energy2, Time(5))
        expected_power = gpu2_power  # In this case it should only count the second gpu
        assert expected_power.kW == gpu.total_power().kW


class TestGpuNotAvailable:
    def setup_method(self):
        self.old_sys_path = copy(sys.path)
        fake_module_path = os.path.join(os.path.dirname(__file__), "fake_modules")
        sys.path.insert(0, fake_module_path)

        # Clean old modules
        try:
            del sys.modules["pynvml"]
        except KeyError:
            pass

        try:
            del sys.modules["codecarbon.core.gpu"]
        except KeyError:
            pass

        import pynvml

        pynvml.INIT_MOCK.side_effect = pynvml.NVMLError("NVML Shared Library Not Found")

    def teardown_method(self):
        import pynvml

        pynvml.INIT_MOCK.reset_mock()

        # Restore the old paths
        sys.path = self.old_sys_path

    def test_is_gpu_details_not_available(self):
        from codecarbon.core.gpu import is_gpu_details_available

        assert is_gpu_details_available() is False

    def test_gpu_details_not_available(self):
        from codecarbon.core.gpu import AllGPUDevices

        alldevices = AllGPUDevices()

        assert alldevices.get_gpu_details() == []

    def test_static_gpu_info_not_available(self):
        from codecarbon.core.gpu import AllGPUDevices

        alldevices = AllGPUDevices()

        assert alldevices.get_gpu_static_info() == []
