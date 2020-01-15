#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#########################################################################################################################
# Created on 01/14/2020 by Virag Doshi
# Copyright © 2020 Virag Doshi
#
#########################################################################################################################

import os
import tarfile
import unittest, random, filecmp


class Tar(object):
    @staticmethod
    def tarDir(inDir, outFile):
        with tarfile.open(outFile, 'w|gz') as tarBall:
            tarBall.add(inDir, arcname = os.path.basename(os.path.normpath(inDir)))

    @staticmethod
    def untar(inBall, outPath):
        with tarfile.open(inBall, 'r') as tarBall:
            tarBall.extractall(outPath)



#########################################################################################################################
# Testing
#########################################################################################################################


class _TarTests(unittest.TestCase):
    def testTarUntarDir(self):
        inTarDir    = '/tmp/inTar/'
        inFiles     = [ 'test1.txt', 'test2.txt', 'test3.txt', 'test4.txt', 'test5.txt']
        outTar      = '/tmp/outTar.tgz'
        outUntarDir = '/tmp/outUntar/'

        if not os.path.exists(inTarDir):
            os.makedirs(inTarDir)

        if not os.path.exists(outUntarDir):
            os.makedirs(outUntarDir)

        for i in range(100):
            for fineName in inFiles:
                fileSize        = random.randint(0, 1024)
                inputStr        = os.urandom(fileSize)

                with open(inTarDir + fineName, 'w') as fIn:
                    fIn.write(inputStr)

            Tar.tarDir(inTarDir, outTar)
            Tar.untar(outTar, outUntarDir)

            dCmp = filecmp.dircmp(inTarDir, outUntarDir + os.path.basename(os.path.normpath(inTarDir)))
            self.assertTrue(len(dCmp.diff_files) is 0)
            self.assertTrue(len(dCmp.same_files) is len(inFiles))


if __name__ == '__main__':
    random.seed()
    unittest.main()
