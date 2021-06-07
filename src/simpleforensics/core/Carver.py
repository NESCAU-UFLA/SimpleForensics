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
from ..structuredData.MBR import MBR
from ..structuredData.GPT import GPT

class Carver:
    def __init__(self, inputPath: str = ""):
        self.ACTIONS = {
            'READ': {
                'MBR': self.readMBR,
                'GPT': self.readGPT,
            },
            'CARVE': {}
        }
        self.__inputPath = inputPath

    def readMBR(self):
        try:
            with open(self.__inputPath, 'rb') as inputFile:
                firstSector = bytearray(inputFile.read(SECTOR_SIZE))
                if MBR.hasSignature(firstSector):
                    exit(f"{MBR(firstSector)}")
                else:
                    raise Exception("Couldn't identify the MBR")
        except FileNotFoundError:
            raise Exception(f"{self.__inputPath} not found")
    
    def readGPT(self):
        try:
            with open(self.__inputPath, 'rb') as inputFile:
                firstSector = bytearray(inputFile.read(SECTOR_SIZE))
                secondSector = bytearray(inputFile.read(SECTOR_SIZE))
                if GPT.hasSignature(firstSector, secondSector):
                    exit(f"{GPT(secondSector, bytearray(inputFile.read(SECTOR_SIZE*32)))}")
                else:
                    raise Exception("Couldn't identify the GPT")
        except FileNotFoundError:
            raise Exception(f"{self.__inputPath} not found")