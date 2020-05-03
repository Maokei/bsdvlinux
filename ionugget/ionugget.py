#!/usr/bin/env python
'''
Tested with python 3.7
'''
import os, sys, argparse
from time import perf_counter as time
import uuid
import random

NUGGET_BANNER = r'''
 _                                    _   
(_) ___  _ __  _   _  __ _  __ _  ___| |_ 
| |/ _ \| '_ \| | | |/ _` |/ _` |/ _ \ __|
| | (_) | | | | |_| | (_| | (_| |  __/ |_ 
|_|\___/|_| |_|\__,_|\__, |\__, |\___|\__|
                     |___/ |___/              
'''

def getArguments():
    '''
    Parses commandline arguments, the following flags exists:
        --size
    '''
    argparser = argparse.ArgumentParser(description='IONugget arguments')
    argparser.add_argument('-s',
                            '--size',
                            required=False,
                            action='store',
                            type=int,
                            default=128,
                            help="Size of the file to be written")
    argparser.add_argument('-i'
                            '--iterations',
                            required=False,
                            type=int,
                            default=1,
                            help="Number of iterations")
    return argparser.parse_args()

class IOTest:
    '''
    Class contains all methods needed to run a IO test
    '''
    def __init__(self, fileSizeMb):
        self.tempFile = "/tmp/test"
        self.permission = 0o777
        self.wBlockSizeKb = 1024
        self.rBlockSizeKb = 512
        self.fileSizeMb = fileSizeMb
        self.wCount=int((self.fileSizeMb * 1024) / self.wBlockSizeKb)
        self.rCount=int((self.fileSizeMb * 1024 * 1024) / self.rBlockSizeKb)

    def run(self):
        print("run: ", self.tempFile)
        writeRes = self.writeTestFile(self.wBlockSizeKb * 1024, self.wCount)
        readRes = self.readTestFile(self.rBlockSizeKb, self.rCount)
        #write
        writeTime = sum(writeRes)
        writeAvg = (self.fileSizeMb / writeTime)
        wMax = self.wBlockSizeKb / (1024 * min(writeRes))
        wMin = self.wBlockSizeKb / (1024 * max(writeRes))
        print(writeTime)
        print(writeAvg)
        print(wMax)
        print(wMin)
        print("")
        readTime = sum(readRes)
        readAvg = (self.fileSizeMb / readTime)
        rMax = self.rBlockSizeKb / (1024 * 1024 * min(readRes))
        rMin = self.rBlockSizeKb / (1024 * 1024 * max(readRes))
        print(readTime)
        print(readAvg)
        print(rMax)
        print(rMin)


        self.handleResults()

    def writeTestFile(self, blockSize, blockCount):
        '''
        Writes the file to the disk, file consisting of random data
        
        return write time for each block list
        '''
        print("blocksize: ", blockSize)
        print("blockCount: ", blockCount)
        fl = os.open(self.tempFile, os.O_CREAT | os.O_WRONLY, self.permission)

        result = []
        for i in range(blockCount):
            fileBuffer = os.urandom(blockSize) # random block of data
            startTime = time()
            os.write(fl, fileBuffer)
            os.fsync(fl)
            diff = time() - startTime
            result.append(diff)

        os.close(fl)
        return result
    
    def readTestFile(self, blockSize, blockCount):
        '''
        Reads the temporary file, times the reading
        of the file until it reaches the end.

        returs read time for each block list
        '''
        print("blocksize: ", blockSize)
        print("blockcount ", blockCount)
        fl = os.open(self.tempFile, os.O_RDONLY, self.permission)
        offsets = list(range(0, (blockCount * blockSize), blockSize))
        random.shuffle(offsets)
        
        result = []
        for i, offset in enumerate(offsets, 1):
            start = time()
            os.lseek(fl, offset, os.SEEK_SET)  # set position
            buff = os.read(fl, blockSize)  # read from position
            t = time() - start
            if not buff: break  # if EOF reached
            result.append(t)

        os.close(fl)
        os.remove(self.tempFile)
        return result
    
    def handleResults(self):
        print("handle results TODO")

    def getFilename(self):
        return str(uuid.uuid4())

    def outputResults(self):
        print("Outputing results")


def main():
    print(NUGGET_BANNER)
    arguments = getArguments()
    print("arguments: ", arguments)
    #Create on test
    ioTest = IOTest(arguments.size)
    ioTest.run()



if __name__ == "__main__":
    main()