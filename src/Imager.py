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

import hashlib

CLUSTER_SIZE = 512

class Imager:
    def __init__(self, inputPath: str = "", outputPath: str = ""):
        self.__inputPath = inputPath
        self.__outputPath = outputPath
        self.__hashes = {
            'input': {
                'md5': "",
                'sha1': "",
            },
            'output': {
                'md5': "",
                'sha1': "",
            }
        }
    
    def copy(self):
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        with open(self.__inputPath, 'rb') as inputFile:
            with open(self.__outputPath, 'wb') as outputFile:
                data = inputFile.read(CLUSTER_SIZE)
                while data:
                    md5.update(data)
                    sha1.update(data)
                    outputFile.write(data)
                    data = inputFile.read(CLUSTER_SIZE)
        self.__hashes['input'] = {
            'md5': md5.hexdigest(),
            'sha1': sha1.hexdigest(),
        }
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        with open(self.__outputPath, 'rb') as outputFile:
            data = inputFile.read(CLUSTER_SIZE)
            while data:
                md5.update(data)
                sha1.update(data)
                data = outputFile.read(CLUSTER_SIZE)
        self.__hashes['output'] = {
            'md5': md5.hexdigest(),
            'sha1': sha1.hexdigest(),
        }