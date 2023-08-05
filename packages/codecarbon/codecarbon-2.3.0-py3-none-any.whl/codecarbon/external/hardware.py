"""
Encapsulates external dependencies to retrieve hardware metadata
"""

import os
import re
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import psutil

from codecarbon.core.cpu import IntelPowerGadget, IntelRAPL
from codecarbon.core.gpu import AllGPUDevices
from codecarbon.core.units import Energy, Power, Time
from codecarbon.core.util import detect_cpu_model
from codecarbon.external.logger import logger

# default W value for a CPU if no model is found in the ref csv
POWER_CONSTANT = 85

#  ratio of TDP estimated to be consumed on average
CONSUMPTION_PERCENTAGE_CONSTANT = 0.5

B_TO_GB = 1024 * 1024 * 1024  # Or 1e9 ?


@dataclass
class BaseHardware(ABC):
    @abstractmethod
    def total_power(self) -> Power:
        pass

    def description(self) -> str:
        return repr(self)

    def measure_power_and_energy(self, last_duration: float) -> Tuple[Power, Energy]:
        """
        Base implementation: we get the power from the
        hardware and convert it to energy.
        """
        power = self.total_power()
        energy = Energy.from_power_and_time(
            power=power, time=Time.from_seconds(last_duration)
        )
        return power, energy

    def start(self) -> None:
        pass


@dataclass
class GPU(BaseHardware):
    gpu_ids: Optional[List]

    def __repr__(self) -> str:
        return super().__repr__() + " ({})".format(
            ", ".join([d["name"] for d in self.devices.get_gpu_details()])
        )

    def __post_init__(self):
        self.devices = AllGPUDevices()
        self.num_gpus = self.devices.device_count
        self._total_power = Power(
            0  # It will be 0 until we call for the first time measure_power_and_energy
        )

    def measure_power_and_energy(
        self, last_duration: float, gpu_ids: Iterable[int] = None
    ) -> Tuple[Power, Energy]:
        if not gpu_ids:
            gpu_ids = self._get_gpu_ids()
        all_gpu_details: List[Dict] = self.devices.get_delta(
            Time.from_seconds(last_duration)
        )
        # We get the total energy and power of only the ones in gpu_ids
        total_energy = Energy.from_energy(
            sum(
                [
                    gpu_details["delta_energy_consumption"].kWh
                    for idx, gpu_details in enumerate(all_gpu_details)
                    if idx in gpu_ids
                ]
            )
        )
        self._total_power = Power(
            sum(
                [
                    gpu_details["power_usage"].kW
                    for idx, gpu_details in enumerate(all_gpu_details)
                    if idx in gpu_ids
                ]
            )
        )
        return self._total_power, total_energy

    def _get_gpu_ids(self) -> Iterable[int]:
        """
        Get the Ids of the GPUs that we would like to monitor
        :return: list of ids
        """
        if self.gpu_ids is not None:
            gpu_ids = self.gpu_ids
            assert set(gpu_ids).issubset(
                set(range(self.num_gpus))
            ), f"Unknown GPU ids {gpu_ids}"
        else:
            gpu_ids = set(range(self.num_gpus))
        return gpu_ids

    def total_power(self) -> Power:
        return self._total_power

    def start(self) -> None:
        for d in self.devices.devices:
            d.start()

    @classmethod
    def from_utils(cls, gpu_ids: Optional[List] = None) -> "GPU":
        return cls(gpu_ids=gpu_ids)


@dataclass
class CPU(BaseHardware):
    def __init__(
        self,
        output_dir: str,
        mode: str,
        model: str,
        tdp: int,
        rapl_dir: str = "/sys/class/powercap/intel-rapl",
    ):
        self._output_dir = output_dir
        self._mode = mode
        self._model = model
        self._tdp = tdp
        self._is_generic_tdp = False
        if self._mode == "intel_power_gadget":
            self._intel_interface = IntelPowerGadget(self._output_dir)
        elif self._mode == "intel_rapl":
            self._intel_interface = IntelRAPL(rapl_dir=rapl_dir)

    def __repr__(self) -> str:
        if self._mode != "constant":
            return f"CPU({' '.join(map(str.capitalize, self._mode.split('_')))})"

        s = f"CPU({self._model} > {self._tdp}W"

        if self._is_generic_tdp:
            s += " [generic]"

        return s + ")"

    def _get_power_from_cpus(self) -> Power:
        """
        Get CPU power
        :return: power in kW
        """
        if self._mode == "constant":
            power = self._tdp * CONSUMPTION_PERCENTAGE_CONSTANT
            return Power.from_watts(power)
        if self._mode == "intel_rapl":
            # Don't call get_cpu_details to avoid computing energy twice and losing data.
            all_cpu_details: Dict = self._intel_interface.get_static_cpu_details()
        else:
            all_cpu_details: Dict = self._intel_interface.get_cpu_details()

        power = 0
        for metric, value in all_cpu_details.items():
            # "^Processor Power_\d+\(Watt\)$" for Inter Power Gadget
            if re.match(r"^Processor Power", metric):
                power += value
                logger.debug(f"_get_power_from_cpus - MATCH {metric} : {value}")

            else:
                logger.debug(f"_get_power_from_cpus - DONT MATCH {metric} : {value}")
        return Power.from_watts(power)

    def _get_energy_from_cpus(self, delay: Time) -> Energy:
        """
        Get CPU energy deltas from RAPL files
        :return: energy in kWh
        """
        all_cpu_details: Dict = self._intel_interface.get_cpu_details(delay)

        energy = 0
        for metric, value in all_cpu_details.items():
            if re.match(r"^Processor Energy Delta_\d", metric):
                energy += value
                # logger.debug(f"_get_energy_from_cpus - MATCH {metric} : {value}")
        return Energy.from_energy(energy)

    def total_power(self) -> Power:
        cpu_power = self._get_power_from_cpus()
        return cpu_power

    def measure_power_and_energy(self, last_duration: float) -> Tuple[Power, Energy]:
        if self._mode == "intel_rapl":
            energy = self._get_energy_from_cpus(delay=Time(seconds=last_duration))
            power = self.total_power()
            return power, energy
        # If not intel_rapl
        return super().measure_power_and_energy(last_duration=last_duration)

    def start(self):
        if self._mode in ["intel_power_gadget", "intel_rapl"]:
            self._intel_interface.start()
        pass

    def get_model(self):
        return self._model

    @classmethod
    def from_utils(
        cls,
        output_dir: str,
        mode: str,
        model: Optional[str] = None,
        tdp: Optional[int] = None,
    ) -> "CPU":
        if model is None:
            model = detect_cpu_model()
            if model is None:
                logger.warning("Could not read CPU model.")

        if tdp is None:
            tdp = POWER_CONSTANT
            cpu = cls(output_dir=output_dir, mode=mode, model=model, tdp=tdp)
            cpu._is_generic_tdp = True
            return cpu

        return cls(output_dir=output_dir, mode=mode, model=model, tdp=tdp)


@dataclass
class RAM(BaseHardware):
    # 3 watts of power for every 8GB of DDR3 or DDR4 memory
    # https://www.crucial.com/support/articles-faq-memory/how-much-power-does-memory-use
    power_per_GB = 3 / 8  # W/GB

    def __init__(
        self,
        pid: int = psutil.Process().pid,
        children: bool = True,
        tracking_mode: str = "machine",
    ):
        """
        Instantiate a RAM object from a reference pid. If none is provided, will use the
        current process's. The `pid` is used to find children processes if `children`
        is True.

        Args:
            pid (int, optional): Process id (with respect to which we'll look for
                                 children). Defaults to psutil.Process().pid.
            children (int, optional): Look for children of the process when computing
                                      total RAM used. Defaults to True.
        """
        self._pid = pid
        self._children = children
        self._tracking_mode = tracking_mode

    def _get_children_memories(self):
        """
        Compute the used RAM by the process's children

        Returns:
            list(int): The list of RAM values
        """
        current_process = psutil.Process(self._pid)
        children = current_process.children(recursive=True)
        return [child.memory_info().rss for child in children]

    def _read_slurm_scontrol(self):
        try:
            return subprocess.check_output(
                ["scontrol show job $SLURM_JOBID"], shell=True
            ).decode()
        except subprocess.CalledProcessError:
            return

    def _parse_scontrol_memory_GB(self, mem):
        nb = int(mem[:-1])
        unit = mem[-1]
        if unit == "T":
            return nb * 1000
        if unit == "G":
            return nb
        if unit == "M":
            return nb / 1000
        if unit == "K":
            return nb / (1000**2)

    def _parse_scontrol(self, scontrol_str):
        mem_matches = re.findall(r"mem=\d+[A-Z]", scontrol_str)
        if len(mem_matches) == 0:
            logger.warning(
                "Could not find mem= after running `scontrol show job $SLURM_JOBID` "
                + "to count SLURM-available RAM. Using the machine's total RAM."
            )
            return psutil.virtual_memory().total / B_TO_GB
        if len(mem_matches) > 1:
            logger.warning(
                "Unexpected output after running `scontrol show job $SLURM_JOBID` "
                + "to count SLURM-available RAM. Using the machine's total RAM."
            )
            return psutil.virtual_memory().total / B_TO_GB

        return mem_matches[0].replace("mem=", "")

    @property
    def slurm_memory_GB(self):
        scontrol_str = self._read_slurm_scontrol()
        if scontrol_str is None:
            logger.warning(
                "Error running `scontrol show job $SLURM_JOBID` "
                + "to retrieve SLURM-available RAM."
                + "Using the machine's total RAM."
            )
            return psutil.virtual_memory().total / B_TO_GB
        mem = self._parse_scontrol(scontrol_str)
        if isinstance(mem, str):
            return self._parse_scontrol_memory_GB(mem)
        return mem

    @property
    def process_memory_GB(self):
        """
        Property to compute the process's total memory usage in bytes.

        Returns:
            float: RAM usage (GB)
        """
        children_memories = self._get_children_memories() if self._children else []
        main_memory = psutil.Process(self._pid).memory_info().rss
        memories = children_memories + [main_memory]
        return sum([m for m in memories if m] + [0]) / B_TO_GB

    @property
    def machine_memory_GB(self):
        return (
            self.slurm_memory_GB
            if os.environ.get("SLURM_JOB_ID")
            else psutil.virtual_memory().total / B_TO_GB
        )

    def total_power(self) -> Power:
        """
        Compute the Power (kW) consumed by the current process (and its children if
        `children` was True in __init__)

        Returns:
            Power: kW of power consumption, using self.power_per_GB W/GB
        """
        try:
            memory_GB = (
                self.machine_memory_GB
                if self._tracking_mode == "machine"
                else self.process_memory_GB
            )
            ram_power = Power.from_watts(memory_GB * self.power_per_GB)
        except Exception as e:
            logger.warning(f"Could not measure RAM Power ({str(e)})")
            ram_power = Power.from_watts(0)

        return ram_power
