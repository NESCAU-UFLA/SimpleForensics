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

class Hasher:
    __instance = None

    @staticmethod
    def getInstance():
        if Hasher.__instance == None:
            Hasher()
        return Hasher.__instance

    def __init__(self):
        if Hasher.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Hasher.__instance = self
        self.md5 = hashlib.md5()
        self.sha1 = hashlib.sha1()
    
    def getHashes(self):
        return {
            'md5': self.md5.hexdigest(),
            'sha1': self.sha1.hexdigest(),
        }

    def clear(self):
        self.md5 = hashlib.md5()
        self.sha1 = hashlib.sha1()

    def update(self, data: bytes):
        self.md5.update(data)
        self.sha1.update(data)

hasher = Hasher.getInstance()