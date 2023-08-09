import shutil
from enum import Enum
from pathlib import Path
from typing import Union

from pydantic import constr
from pydantic import root_validator
from pydantic import validate_arguments

from ...testbed_client import tb_client
from ..base.content import ContentModel
from ..testbed.mcu import MCU

try:
    from ... import fw_tools

    elf_support = True
except ImportError:
    elf_support = False


class FirmwareDType(str, Enum):
    base64_hex = "hex"
    base64_elf = "elf"
    path_hex = "path_hex"
    path_elf = "path_elf"


suffix_to_DType: dict = {
    # derived from wikipedia
    ".hex": FirmwareDType.base64_hex,
    ".ihex": FirmwareDType.base64_hex,
    ".ihx": FirmwareDType.base64_hex,
    ".elf": FirmwareDType.base64_elf,
    ".bin": FirmwareDType.base64_elf,
    ".o": FirmwareDType.base64_elf,
    ".out": FirmwareDType.base64_elf,
    ".so": FirmwareDType.base64_elf,
}

arch_to_mcu: dict = {
    "em_msp430": {"name": "msp430fr"},
    "msp430": {"name": "msp430fr"},
    "arm": {"name": "nrf52"},
    "nrf52": {"name": "nrf52"},
}


class Firmware(ContentModel, title="Firmware of Target"):
    """meta-data representation of a data-component"""

    # General Metadata & Ownership -> ContentModel

    mcu: MCU

    data: Union[constr(min_length=3, max_length=8_000_000), Path]
    data_type: FirmwareDType

    # TODO: a data-hash would be awesome

    @root_validator(pre=True)
    def query_database(cls, values: dict) -> dict:
        values, _ = tb_client.try_completing_model(cls.__name__, values)
        return tb_client.fill_in_user_data(values)

    @classmethod
    def from_firmware(cls, file: Path, **kwargs):
        """embeds firmware and tries to fill parameters
        ELF -> mcu und data_type are deducted
        HEX -> must supply mcu manually
        """
        if not elf_support:
            raise RuntimeError(
                "Please install functionality with 'pip install shepherd_core[elf] -U'"
            )
        kwargs["data"] = fw_tools.file_to_base64(file)
        if "data_type" not in kwargs:
            kwargs["data_type"] = suffix_to_DType[file.suffix.lower()]

        if kwargs["data_type"] == FirmwareDType.base64_hex:
            if fw_tools.is_hex_msp430(file):
                arch = "msp430"
            elif fw_tools.is_hex_nrf52(file):
                arch = "nrf52"
            else:
                raise ValueError("File is not a HEX for the Testbed")
            if "mcu" not in kwargs:
                kwargs["mcu"] = arch_to_mcu[arch]

        if kwargs["data_type"] == FirmwareDType.base64_elf:
            arch = fw_tools.read_arch(file)
            if "msp430" in arch and not fw_tools.is_elf_msp430(file):
                raise ValueError("File is not a ELF for msp430")
            if "nrf52" in arch and not fw_tools.is_elf_nrf52(file):
                raise ValueError("File is not a ELF for nRF52")
            if "mcu" not in kwargs:
                kwargs["mcu"] = arch_to_mcu[arch]
        return cls(**kwargs)

    @validate_arguments
    def extract_firmware(self, file: Path) -> Path:
        """stores embedded data in file
        - file-suffix is derived from data-type and adapted
        - if provided path is a directory, the firmware-name is used
        """
        if not elf_support:
            raise RuntimeError(
                "Please install functionality with 'pip install shepherd_core[elf] -U'"
            )
        if file.is_dir():
            file = file / self.name
        if self.data_type == FirmwareDType.base64_elf:
            file = file.with_suffix(".elf")
            fw_tools.base64_to_file(self.data, file)
        elif self.data_type == FirmwareDType.base64_hex:
            file = file.with_suffix(".hex")
            fw_tools.base64_to_file(self.data, file)
        elif isinstance(self.data, Path):
            if self.data_type == FirmwareDType.path_elf:
                file = file.with_suffix(".elf")
            elif self.data_type == FirmwareDType.path_hex:
                file = file.with_suffix(".hex")
            shutil.copy(self.data, file)
        return file
