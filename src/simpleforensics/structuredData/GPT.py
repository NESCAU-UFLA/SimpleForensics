## SimpleForensics
#
# Authors:
#    Vitor Oriel C N Borges <https://github.com/VitorOriel>
# License: MIT (LICENSE.md)
#    Copyright (c) 2021 Vitor Oriel
#    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
## https://github.com/NESCAU-UFLA/SimpleForensics

from .MBR import MBR
from ..utils.Bytes import Bytes
from ..utils.consts import SECTOR_SIZE
from ..utils.utils import *

class GPT:
    @staticmethod
    def hasSignature(
        firstSector: bytearray,
        secondSector: bytearray
    ):
        if MBR.hasSignature(firstSector):
            mbr = MBR(firstSector)
            if mbr.isGptProtection():
                if Bytes.cmp(
                    first=Bytes.get(secondSector, n=8),
                    second=b'\x54\x52\x41\x50\x20\x49\x46\x45',
                    endian='invert'
                ):
                    return True
        return False

    def __init__(self,
        primaryHeader: bytearray,
        registers: bytearray
    ):
        self.primaryHeader = self.__setupHeader(primaryHeader)
        self.partitionsRegisters = self.__setupRegisters([
            Bytes.cut(
                registers, n=self.primaryHeader['REGISTER_ENTRY_SIZE']
            ) for _ in range(self.primaryHeader['NUMBER_OF_PARTITIONS'])
        ])
    
    def __str__(self):
        string = f"\nGPT ({self.primaryHeader['SIGNATURE']})\n\n"
        string += f"HEADER INFORMATION:\n"
        for key, value in self.primaryHeader.items():
            string += f"   {key}: {value}\n"
        string += "\nPARTITION REGISTERS:\n"
        for i, register in enumerate(self.partitionsRegisters):
            string += f"\nREGISTER {i}:\n"
            for key, value in register.items():
                string += f"   {key}: {value}\n"
        return string

    def __setupHeader(self, primaryHeader: bytearray):
        signature = Bytes.toString(Bytes.cut(primaryHeader, n=8))
        revision = Bytes.toString(Bytes.cut(primaryHeader, n=4))
        headerSize = Bytes.sum(Bytes.cut(primaryHeader, n=4))
        crc32_1 = Bytes.toString(Bytes.cut(primaryHeader, n=4))
        Bytes.cut(primaryHeader, n=4) # reserved area
        gptHeaderLocation = Bytes.sum(Bytes.cut(primaryHeader, n=8))
        gptHeaderBackup = Bytes.sum(Bytes.cut(primaryHeader, n=8))
        nextLocationToPartition = Bytes.sum(Bytes.cut(primaryHeader, n=8))
        lastPartition = Bytes.sum(Bytes.cut(primaryHeader, n=8))
        uuid = Bytes.toString(Bytes.cut(primaryHeader, n=16))
        startPartitionsRegisters = Bytes.sum(Bytes.cut(primaryHeader, n=8))
        numberOfPartitions = Bytes.sum(Bytes.cut(primaryHeader, n=4))
        registerTableEntrySize = Bytes.sum(Bytes.cut(primaryHeader, n=4))
        crc32_2 = Bytes.toString(Bytes.cut(primaryHeader, n=4))
        return {
            'SIGNATURE': signature,
            'REVISION': revision,
            'HEADER_SIZE': headerSize,
            'CRC32_1': crc32_1,
            'HEADER_LOCATION': gptHeaderLocation,
            'HEADER_BACKUP': gptHeaderBackup,
            'NEXT_FREE_PARTITION': nextLocationToPartition,
            'LAST_FREE_PARTITION': lastPartition,
            'UUID': uuid,
            'START_PARTITIONS_REGISTERS': startPartitionsRegisters,
            'NUMBER_OF_PARTITIONS': numberOfPartitions,
            'REGISTER_ENTRY_SIZE': registerTableEntrySize,
            'CRC32_2': crc32_2,
        }
    
    def __setupRegisters(self, registers: list):
        registers = [{
            'PARTITION_GUID': Bytes.cut(register, n=16),
            'UNIQUE_PARTITION_GUID': Bytes.cut(register, n=16),
            'FIRST_LBA_SECTOR': Bytes.cut(register, n=8),
            'LAST_LBA_SECTOR': Bytes.cut(register, n=8),
            'PARTITION_ATTRIBUTES': Bytes.cut(register, n=8),
            'PARTITION_NAME': Bytes.cut(register, n=72),
        } for register in registers]
        return [{
            'PARTITION_GUID': Bytes.toString(register['PARTITION_GUID']),
            'UNIQUE_PARTITION_GUID': Bytes.toString(register['UNIQUE_PARTITION_GUID']),
            'FIRST_LBA_SECTOR': Bytes.sum(register['FIRST_LBA_SECTOR']),
            'LAST_LBA_SECTOR': Bytes.sum(register['LAST_LBA_SECTOR']),
            'PARTITION_ATTRIBUTES': Bytes.toString(register['PARTITION_ATTRIBUTES']),
            'PARTITION_NAME': Bytes.toString(register['PARTITION_NAME'], charset='utf-16'),
        } for register in registers if not Bytes.isEmpty(register['PARTITION_GUID'])]