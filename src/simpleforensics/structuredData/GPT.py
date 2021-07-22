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
        self.partitionsRegisters = [
            Bytes.cut(
                registers, n=self.primaryHeader['REGISTER_ENTRY_SIZE']
            ) for _ in self.primaryHeader['NUMBER_OF_PARTITIONS']
        ]
    
    def __str__(self):
        ph = self.primaryHeader
        string = f"\nGPT (ass {ph['SIGNATURE']})\n\n"
        string += f"HEADER INFORMATION:\n"
        string += f"   REVISION: {ph['REVISION']}\n"
        string += f"   HEADER SIZE: {ph['HEADER_SIZE']}\n"
        string += f"   FIRST CRC32: {ph['CRC32_1']}\n"
        string += f"   HEADER LOCATION: {ph['HEADER_LOCATION']}\n"
        string += f"   HEADER BACKUP LOCATION: {ph['HEADER_LOCATION']}\n"
        string += f"   NEXT FREE SPACE TO PARTITION: {ph['NEXT_FREE_PARTITION']}\n"
        string += f"   LAST FREE SPACE TO PARTITION: {ph['LAST_FREE_PARTITION']}\n"
        string += f"   UUID: {ph['UUID']}\n"
        string += f"   START OF PARTITIONS REGISTERS: {ph['START_PARTITIONS_REGISTERS']}\n"
        string += f"   NUMBER OF PARTITIONS: {ph['NUMBER_OF_PARTITIONS']}\n"
        string += f"   REGISTERS ENTRY SIZE: {ph['REGISTER_ENTRY_SIZE']}\n"
        string += f"   SECOND CRC32: {ph['CRC32_2']}\n\n"

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