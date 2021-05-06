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

from .Hasher import hasher
from .utils.consts import SECTOR_SIZE
from .structuredData.MBR import MBR

class Imager:
    def __init__(self, inputPath: str = "", outputPath: str = ""):
        self.__inputPath = inputPath
        self.__outputPath = outputPath
        self.BUFFER_SIZE = SECTOR_SIZE
        self.BLOCKS_COUNT = 0
        self.hashes = {
            'input': {},
            'output': {}
        }

    def copy(self):
        hasher.clear()
        try:
            with open(self.__inputPath, 'rb') as inputFile:
                with open(self.__outputPath, 'wb') as outputFile:
                    data = inputFile.read(self.BUFFER_SIZE)
                    i = 1
                    stop = False
                    while data and not stop:
                        hasher.update(data)
                        outputFile.write(data)
                        if i == self.BLOCKS_COUNT:
                            stop = True
                        data = inputFile.read(self.BUFFER_SIZE)
                        i += 1
        except FileNotFoundError:
            raise Exception(f"{self.__inputPath} not found")
        self.hashes['input'] = hasher.getHashes()

    def checkIntegrity(self):
        hasher.clear()
        try:
            with open(self.__outputPath, 'rb') as outputFile:
                data = outputFile.read(self.BUFFER_SIZE)
                while data:
                    hasher.update(data)
                    data = outputFile.read(self.BUFFER_SIZE)
        except FileNotFoundError:
            raise Exception(f"{self.__outputPath} not found")
        self.hashes['output'] = hasher.getHashes()
        return self.hashes['input'] == self.hashes['output']

    def wipe(self):
        try:
            with open(self.__outputPath, 'r+b') as outputFile:
                data = outputFile.read(self.BUFFER_SIZE)
                ACTUAL_BUFFER_SIZE = self.BUFFER_SIZE
                while data:
                    if len(data) < self.BUFFER_SIZE:
                        ACTUAL_BUFFER_SIZE = len(data)
                    outputFile.seek(outputFile.tell()-ACTUAL_BUFFER_SIZE)
                    outputFile.write(b'\x00'*ACTUAL_BUFFER_SIZE)
                    data = outputFile.read(self.BUFFER_SIZE)
        except FileNotFoundError:
            raise Exception(f"{self.__outputPath} not found")

    def getMBR(self):
        try:
            with open(self.__inputPath, 'rb') as inputFile:
                firstSector = bytearray(inputFile.read(SECTOR_SIZE))
                if MBR.hasSignature(firstSector):
                    exit(f"{MBR(firstSector)}")
                else:
                    raise Exception("Couldn't identify the MBR")
        except FileNotFoundError:
            raise Exception(f"{self.__inputPath} not found")