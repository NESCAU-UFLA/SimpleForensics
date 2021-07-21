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

from ..utils.Bytes import Bytes
from ..utils.consts import SECTOR_SIZE
from ..utils.utils import *

class MBR:
    @staticmethod
    def hasSignature(sector: bytearray):
        return Bytes.cmp(
            first=Bytes.get(sector, i=510, n=2),
            second=b'\x55\xAA',
        )

    FILESYSTEM_MAP = {
        b'\x00': "No file system or partition",
        b'\x01': "FAT12",
        **dict.fromkeys([b'\x04', b'\x06'], "FAT16 with CHS mapping"),
        b'\x08': "FAT12 or FAT16 with LBA mapping",
        b'\x07': "NTFS or exFAT",
        b'\x0B': "FAT32 with CHS mapping",
        b'\x0C': "FAT32 with LBA mapping",
        b'\x82': "Linux swap partition",
        b'\x83': "Native linux filesystem partition",
        b'\x8E': "Linux Logical Volume Manager (LVM)",
        b'\x96': "ISO-9660",
        b'\xAF': "HFS or HFS+",
        b'\xEE': "MBR protection for GPT",
    }

    def __init__(self, sector: bytearray):
        self.bootCode = Bytes.cut(sector, n=440)
        self.diskSignature = Bytes.cut(sector, n=4)
        self.writeProtection = Bytes.cut(sector, n=2)
        self.partitionsTable = [{
            'IS_BOOTABLE': Bytes.cut(sector, n=1),
            'CHS_MAP_1': Bytes.cut(sector, n=3),
            'TYPE': Bytes.cut(sector, n=1),
            'CHS_MAP_2': Bytes.cut(sector, n=3),
            'LBA_MAP': Bytes.cut(sector, n=4),
            'LENGTH': Bytes.cut(sector, n=4)
        } for _ in range(4)]
        self.signature = Bytes.cut(sector, n=2)

    def __str__(self):
        string = f"MBR INFORMATION (ass {Bytes.toString(self.signature)}):\n\n"
        string += f"DISK SIGNATURE: {Bytes.toString(self.diskSignature)}\n"
        string += f"WRITE PROTECTION ENABLED: {self.hasWriteProtection()}\n\n"
        for i, p in enumerate(self.partitionsTable):
            string += f"Partition {i+1}\n"
            string += f"   Is bootable: {self.partitionIsBootable(p['IS_BOOTABLE'])}\n"
            string += f"   First CHS map: {Bytes.toString(p['CHS_MAP_1'])}\n"
            string += f"   Type: {self.getFileSystem(p['TYPE'])}\n"
            string += f"   Second CHS map: {Bytes.toString(p['CHS_MAP_2'])}\n"
            string += f"   LBA map: {Bytes.toString(p['LBA_MAP'])}\n"
            string += f"   Length: {convertToGigabyte(convertSectorsToBytes(Bytes.sum(p['LENGTH'])))} GiB\n\n"
        return string

    def partitionIsBootable(self, flag: bytearray):
        if flag == b'\x80':
            return 'YES'
        elif flag == b'\x00':
            return 'NO'
        return '?'

    def hasWriteProtection(self):
        flag = self.writeProtection
        if flag == b'\x5A\x5A':
            return 'YES'
        elif flag == b'\x00\x00':
            return 'NO'
        return '?'

    def getFileSystem(self, flag: bytearray):
        try:
            return MBR.FILESYSTEM_MAP[bytes(flag)]
        except:
            return '?'
    
    def isGptProtection(self):
        for table in self.partitionsTable:
            if table['TYPE'] == b'\xEE':
                return True
        return False