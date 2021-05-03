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

from Hasher import hasher

CLUSTER_SIZE = 512

class Imager:
    def __init__(self, inputPath: str = "", outputPath: str = ""):
        self.__inputPath = inputPath
        self.__outputPath = outputPath
        self.hashes = {
            'input': {},
            'output': {}
        }
    
    def copy(self):
        hasher.clear()
        with open(self.__inputPath, 'rb') as inputFile:
            with open(self.__outputPath, 'wb') as outputFile:
                data = inputFile.read(CLUSTER_SIZE)
                i = 1
                while data:
                    hasher.update(data)
                    outputFile.write(data)
                    #print(f"Copied: {i*CLUSTER_SIZE} bytes")
                    data = inputFile.read(CLUSTER_SIZE)
                    i += 1
        self.hashes['input'] = hasher.getHashes()
    
    def checkIntegrity(self):
        hasher.clear()
        with open(self.__outputPath, 'rb') as outputFile:
            data = outputFile.read(CLUSTER_SIZE)
            while data:
                hasher.update(data)
                data = outputFile.read(CLUSTER_SIZE)
        self.hashes['output'] = hasher.getHashes()
        if self.hashes['input'] == self.hashes['output']:
            return True
        return False