#!/usr/bin/python3

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

from .Imager import Imager

import sys

class CLIParser:
    def __init__(self):
        self.__argv = sys.argv
        self.instanceArgs()
    
    def instanceArgs(self):
        self.inputPath = ''
        self.outputPath = None
        self.bufferSize = None
        self.count = None
        for arg in self.__argv:
            if 'if=' in arg:
                self.inputPath = arg.split('=')[1]
            if 'of=' in arg:
                self.outputPath = arg.split('=')[1]
            if 'bs=' in arg:
                try:
                    self.bufferSize = int(arg.split('=')[1])
                except:
                    exit("Buffer size must be an integer")
                if not ((self.bufferSize & (self.bufferSize-1) == 0) and self.bufferSize != 0):
                    exit("Buffer size must be power of 2")
            if 'count=' in arg:
                try:
                    self.count = int(arg.split('=')[1])
                    if self.count < 1:
                        raise Exception()
                except:
                    exit("Quantity of blocks must be a positive integer, greater than 0")
        if not self.outputPath:
            exit("At least an outputPath file is needed")
    
    def getFilePaths(self):
        return (self.inputPath, self.outputPath)
    
    def checkBlocksCount(self, imager: Imager):
        if self.count:
            imager.BLOCKS_COUNT = self.count

    def checkBufferSize(self, imager: Imager):
        if self.bufferSize:
            imager.BUFFER_SIZE = self.bufferSize

    def isWipe(self):
        return '--wipe' in self.__argv