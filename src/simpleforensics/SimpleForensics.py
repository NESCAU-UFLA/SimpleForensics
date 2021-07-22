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

def main_imager():
    from .interfaces.cli.imager.CliArguments import CliArguments
    from .core.Imager import Imager
    arguments = CliArguments()
    inputPath, outputPath = arguments.getFilePaths()
    imager = Imager(inputPath, outputPath)
    if arguments.count:
        imager.BLOCKS_COUNT = arguments.count
    if arguments.bufferSize:
        imager.BUFFER_SIZE = arguments.bufferSize
    try:
        if arguments.isWipe():
            if not outputPath:
                raise Exception("Must set the output file to be wiped!")
            imager.wipe()
            print("Disk wiped!")
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
            for key, value in imager.hashes['input'].items():
                print(f"{key.upper()}: {value}")
            print('')
            print("Output hashes:")
            for key, value in imager.hashes['output'].items():
                print(f"{key.upper()}: {value}")
            print('')
    except PermissionError:
        exit("You need root permissions to read this device")
    except Exception as e:
        exit(str(e))

def main_carver():
    def getAction(arguments):
        for key, value in arguments.reader.items():
            if value:
                return ('READ', key)
        for key, value in arguments.carver.items():
            if value:
                return ('CARVE', key)
        raise Exception("No action specified")

    from .interfaces.cli.carver.CliArguments import CliArguments
    from .core.Carver import Carver
    arguments = CliArguments()
    carver = Carver(arguments.input)
    action, searchFor = getAction(arguments)
    carver.ACTIONS[action][searchFor]()