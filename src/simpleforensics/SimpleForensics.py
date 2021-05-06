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

from .core.Imager import Imager
from .CLIParser import CLIParser

def main():
    parser = CLIParser()
    inputPath, outputPath = parser.getFilePaths()
    imager = Imager(inputPath, outputPath)
    parser.checkBufferSize(imager)
    parser.checkBlocksCount(imager)
    try:
        if parser.isWipe():
            imager.wipe()
            print("Disk wiped!")
        elif parser.isMbrRead():
            imager.readMBR()
        else:
            imager.copy()
            if imager.checkIntegrity():
                print("Success!")
            else:
                print("Failed!")
            if not imager.BLOCKS_COUNT:
                print("\nInput hashes:")
            else:
                print(f"\nInput hashes for the first {imager.BLOCKS_COUNT} blocks:")
            print(f"MD5: {imager.hashes['input']['md5']}")
            print(f"SHA1: {imager.hashes['input']['sha1']}\n")
            print("Output hashes:")
            print(f"MD5: {imager.hashes['output']['md5']}")
            print(f"SHA1: {imager.hashes['output']['sha1']}\n")
    except PermissionError:
        exit("You need root permissions to read this device")
    except Exception as e:
        exit(str(e))