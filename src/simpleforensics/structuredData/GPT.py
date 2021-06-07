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
            for i in range(len(mbr.partitionsTable)):
                if mbr.partitionsTable[i]['TYPE'] == b'\xEE':
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
        self.primaryHeader = primaryHeader
        self.partitionsRegisters = [
            Bytes.cut(registers, n=128) for _ in range(4) for _ in range(32)
        ]