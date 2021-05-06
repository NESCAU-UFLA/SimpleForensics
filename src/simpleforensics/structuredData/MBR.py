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

from ..utils.consts import SECTOR_SIZE
from ..utils.utils import *

class MBR:
    @staticmethod
    def hasSignature(sector: bytearray):
        return getBytes(sector, i=510, n=2) == b'\x55\xAA'

    def __init__(self, sector: bytearray):
        self.bootCode = cutBytes(sector, n=440)
        self.diskSignature = cutBytes(sector, n=4)
        self.writeProtection = cutBytes(sector, n=2)
        self.partitionsTable = [{
            'IS_BOOTABLE': cutBytes(sector, n=1),
            'CHS_MAP_1': cutBytes(sector, n=3),
            'TYPE': cutBytes(sector, n=1),
            'CHS_MAP_2': cutBytes(sector, n=3),
            'LBA_MAP': cutBytes(sector, n=4),
            'LENGTH': cutBytes(sector, n=4)
        } for i in range(4)]
        self.signature = cutBytes(sector, n=2)

    def __str__(self):
        string = f"MBR INFORMATION (ass {bytesToStr(self.signature)}):\n\n"
        string += f"DISK SIGNATURE: {bytesToStr(self.diskSignature)}\n"
        string += f"WRITE PROTECTION ENABLED: {self.hasWriteProtection()}\n\n"
        for i, p in enumerate(self.partitionTable):
            string += f"Partition {i+1}\n"
            string += f"   Is bootable: {self.partitionIsBootable(p['IS_BOOTABLE'])}\n"
            string += f"   First CHS map: {bytesToStr(p['CHS_MAP_1'])}\n"
            string += f"   Type: {self.getFileSystem(p['TYPE'])}\n"
            string += f"   Second CHS map: {bytesToStr(p['CHS_MAP_2'])}\n"
            string += f"   LBA map: {bytesToStr(p['LBA_MAP'])}\n"
            string += f"   Length: {convertToGigabyte(convertSectorsToBytes(sumBytes(p['LENGTH'])))} GiB\n\n"
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
        if flag == b'\x00':
            return "No file system or partition"
        elif flag == b'\x01':
            return "FAT12"
        elif flag == b'\x04' or flag == b'\x06':
            return "FAT16 with CHS mapping"
        elif flag == b'\x08':
            return "FAT12 or FAT16 with LBA mapping"
        elif flag == b'\x07':
            return "NTFS or exFAT"
        elif flag == b'\x0B':
            return "FAT32 with CHS mapping"
        elif flag == b'\x0C':
            return "FAT32 with LBA mapping"
        elif flag == b'\x82':
            return "Linux swap partition"
        elif flag == b'\x83':
            return "Native linux filesystem partition"
        elif flag == b'\x8E':
            return "Linux Logical Volume Manager (LVM)"
        elif flag == b'\x96':
            return "ISO-9660"
        elif flag == b'\xAF':
            return "HFS or HFS+"
        elif flag == b'\xEE':
            return "MBR protection for GPT"
        return '?'