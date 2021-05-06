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

from .consts import *

"""bytearray functions"""
def getBytes(bytesToSearch: bytearray, i: int = 0, n: int = 1) -> bytearray:
    return bytesToSearch[i:(i+n)]

def cutBytes(bytesToCut: bytearray, i: int = 0, n: int = 1) -> bytearray:
    cutedBytes = getBytes(bytesToCut, i, n)
    bytesToCut[:] = bytesToCut[:i] + bytesToCut[(i+n):]
    return cutedBytes

def sumBytes(bytesToSum: bytearray) -> int:
    sumBytes = 0
    for i in range(len(bytesToSum)):
        sumBytes |= bytesToSum[i]<<(8*i)
    return sumBytes

"""converters"""
def bytesToStr(bytesToStr: bytearray) -> str:
    return f"0x{bytesToStr.hex().upper()}"

def convertSectorsToBytes(sectors: int) -> int:
    return sectors*SECTOR_SIZE

def convertToGigabyte(byte: int) -> int:
    return byte/GIGABYTE