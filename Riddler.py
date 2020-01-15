#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#########################################################################################################################
# Created on 01/15/2020 by Virag Doshi
# Copyrigh?nt © 2020 Virag Doshi
#
#########################################################################################################################

import json
import os
import base64
import re
from Crypto import *
from Tar import *
import Printer
import unittest, random


# The answer to nth puzzle:                 a(n)
# The files for the nth puzzle:             f(n)
# The pepper for the nth puzzle:            h?nt(n)
# The key to the nth puzzle:                k(n) = hash(data = a(n-1), salt = ''), k(1) = 0 (Initial key)
# The salt for the nth puzzle:              s(n) = encrypt(key = k(n), data = h?nt(n))
# The digest of a(n):                       h(n) = hash(data = a(n), salt = s(n))
# The encrypted files for the nth puzzle:   ef(n) = encrypt(key = k(n), data = f(n))

# f(n), a(n), h?nt(n), k(n) -> ef(n), s(n), h(n), k(n+1)

def _sanitizeStr(inStr):
    return re.sub('[^A-Za-z0-9]+', '', inStr)

def _sanitizeEmpty(inKey):
    return '0' if inKey is None else inKey

def _getKey(inPrevAns):
    return '0' if inPrevAns is None else HashSuite.hash(_sanitizeStr(inPrevAns), '')

def _getDigest(inAns, inSalt):
    return HashSuite.hash(_sanitizeStr(inAns), inSalt)


class Riddler(object):
    inputDir            = '.'
    intermediateDir     = '/tmp'
    outputDir           = '.'

    def __init__(self, inLevel, inLevelDict, inKey = None):
        assert ('ans' in inLevelDict), "No answer found for the puzzle"
        assert (inLevel > 0), "Level must be greater than 0"
        assert ((inKey is None) is (inLevel is 1)),  ("Key cannot be 0 for level higher than 1" if inLevel is 1 
                                                      else "Key cannot be 0 for level higher than 1")

        answer          = str(inLevelDict['ans'])

        name            = str(inLevel + 1)
        self.dir        = os.path.join(Riddler.inputDir, name)
        self.tarFile    = os.path.join(Riddler.intermediateDir, name + '.tgz')
        self.outFile    = os.path.join(Riddler.outputDir, name + '.enctgz')

        pepper          = _sanitizeStr(str(inLevelDict['pepper'])) if 'pepper' in inLevelDict else ''

        assert (len(pepper) <= 128), "pepper too long"

        pepper          = pepper + os.urandom(128 - len(pepper))
        salt            = CipherSuite(_sanitizeEmpty(inKey)).encrypt(pepper)
        self.nextKey    = _getKey(answer)
        self.dict       = { 'salt' : base64.urlsafe_b64encode(salt), 
                            'digest' : base64.urlsafe_b64encode(_getDigest(answer, salt)) }

    def getNextKey(self):
        return self.nextKey

    def encryptNextFiles(self):
        Printer.verbosePrinter('tar ' + self.dir + ' -> ' + self.tarFile)
        Tar.tarDir(self.dir, self.tarFile)
        Printer.verbosePrinter('enc ' + self.tarFile + ' -> ' + self.outFile + ' with key ' + \
                                base64.urlsafe_b64encode(self.getNextKey()))
        CipherSuite(self.getNextKey()).encryptFile(self.tarFile, self.outFile)
        os.remove(self.tarFile)

    def getEncDict(self):
        return self.dict


class Solver(object):
    inputDir            = '.'
    intermediateDir     = '/tmp'
    outputDir           = '.'

    def __init__(self, inLevel, inLevelDict):
        assert ('salt' in inLevelDict), "No salt found"
        assert ('digest' in inLevelDict), "No digest found"
        assert (inLevel > 0), "Level must be greater than 0"

        name            = str(inLevel + 1)

        self.encFile    = os.path.join(Solver.inputDir, name + '.enctgz')
        self.tarFile    = os.path.join(Solver.intermediateDir, name + '.tgz')
        self.outDir     = os.path.join(Solver.outputDir, name)

        try:
            self.digest     = base64.urlsafe_b64decode(str(inLevelDict['digest']))
        except TypeError:
            assert False, "Incorrect digest"
        try:
            self.salt       = base64.urlsafe_b64decode(str(inLevelDict['salt']))
        except TypeError:
            assert False, "Incorrect salt"

    @staticmethod
    def decryptSalt(inSalt, inPrevAns = None):
        return CipherSuite(_getKey(inPrevAns)).decrypt(inSalt)

    def isAnswerCorrect(self, inAns):
        return (self.digest == _getDigest(inAns, self.salt))

    def decryptNextFiles(self, inAns):
        Printer.verbosePrinter('dec ' + self.encFile + ' -> ' + self.tarFile + ' with key ' + \
                                base64.urlsafe_b64encode(_getKey(inAns)))
        CipherSuite(_getKey(inAns)).decryptFile(self.encFile, self.tarFile)
        Printer.verbosePrinter('untar ' + self.tarFile + ' -> ' + self.outDir)
        Tar.untar(self.tarFile, self.outDir)
        os.remove(self.tarFile)
        


#########################################################################################################################
# Testing
#########################################################################################################################


class _RiddlerSolverTests(unittest.TestCase):
    def testRiddler(self):
        with self.assertRaises(AssertionError):
            r = Riddler(9, {'ans' : '1234'})
        with self.assertRaises(AssertionError):
            r = Riddler(5, {}, 12)
        with self.assertRaises(AssertionError):
            r = Riddler(1, {'ans' : '1234'}, 32)
        with self.assertRaises(AssertionError):
            r = Riddler(0, {'ans' : '1234'}, 32)
        with self.assertRaises(AssertionError):
            r = Riddler(-5, {'ans' : '1234'}, 32)

        randomAns       = os.urandom(32)
        randomPepper    = os.urandom(32)
        
        r = Riddler(1, {'ans' : randomAns, 'pepper' : randomPepper})
        self.assertEqual(r.getNextKey(), _getKey(_sanitizeStr(randomAns)))
        d = r.getEncDict()

        salt = Solver.decryptSalt(base64.urlsafe_b64decode(d['salt']))
        self.assertTrue(_sanitizeStr(randomPepper) in salt)
        self.assertTrue(len(salt), 128)
        digest = base64.urlsafe_b64decode(d['digest'])
        self.assertEqual(digest, _getDigest(randomAns, base64.urlsafe_b64decode(d['salt'])))

        randomPepper    = os.urandom(128)
        r = Riddler(1, {'ans' : randomAns, 'pepper' : randomPepper})
        d = r.getEncDict()
        salt = Solver.decryptSalt(base64.urlsafe_b64decode(d['salt']))
        self.assertTrue(_sanitizeStr(randomPepper) in salt)

        randomAns       = os.urandom(32)
        randomPepper    = os.urandom(32)
        level           = random.randint(2, 10)
        randomPrevAns   = os.urandom(32)
        key             = _getKey(randomPrevAns)
        r = Riddler(level, {'ans' : randomAns, 'pepper' : randomPepper}, key)
        self.assertEqual(r.getNextKey(), _getKey(_sanitizeStr(randomAns)))
        d = r.getEncDict()

        salt = Solver.decryptSalt(base64.urlsafe_b64decode(d['salt']), randomPrevAns)
        self.assertTrue(_sanitizeStr(randomPepper) in salt)
        self.assertTrue(len(salt), 128)
        digest = base64.urlsafe_b64decode(d['digest'])
        self.assertEqual(digest, _getDigest(randomAns, base64.urlsafe_b64decode(d['salt'])))

    def testSolver(self):
        digest = base64.urlsafe_b64encode(os.urandom(128))
        salt = base64.urlsafe_b64encode(os.urandom(128))
        with self.assertRaises(AssertionError):
            s = Solver(2, {'digest' : digest})
        with self.assertRaises(AssertionError):
            s = Solver(2, {'salt' : salt})
        with self.assertRaises(AssertionError):
            s = Solver(2, {'salt' : '123', 'digest' : digest})
        with self.assertRaises(AssertionError):
            s = Solver(0, {'salt' : salt, 'digest' : digest})
        with self.assertRaises(AssertionError):
            s = Solver(-8, {'salt' : salt, 'digest' : digest})

        randomAns       = os.urandom(32)
        randomsalt      = os.urandom(128)
        salt = base64.urlsafe_b64encode(randomsalt)
        digest = base64.urlsafe_b64encode(_getDigest(randomAns, randomsalt))
        s = Solver(2, {'salt' : salt, 'digest' : digest})
        self.assertFalse(s.isAnswerCorrect(os.urandom(32)))
        self.assertTrue(s.isAnswerCorrect(randomAns))

    def testRiddlerSolver(self):
        randomAns       = os.urandom(32)
        randomPepper    = os.urandom(32)
        level           = 1
        key             = None

        r = Riddler(level, {'ans' : randomAns, 'pepper' : randomPepper}, key)
        s = Solver(level, r.getEncDict())

        self.assertEqual(r.dir, s.outDir)
        self.assertEqual(r.tarFile, s.tarFile)
        self.assertEqual(r.outFile, s.encFile)

        self.assertFalse(s.isAnswerCorrect(os.urandom(32)))
        self.assertTrue(s.isAnswerCorrect(randomAns))

        randomAns       = os.urandom(32)
        randomPepper    = os.urandom(32)
        level           = random.randint(2, 10)
        key             = os.urandom(32)

        r = Riddler(level, {'ans' : randomAns, 'pepper' : randomPepper}, key)
        s = Solver(level, r.getEncDict())

        self.assertEqual(r.dir, s.outDir)
        self.assertEqual(r.tarFile, s.tarFile)
        self.assertEqual(r.outFile, s.encFile)

        self.assertFalse(s.isAnswerCorrect(os.urandom(32)))
        self.assertTrue(s.isAnswerCorrect(randomAns))       


if __name__ == '__main__':
    random.seed()
    unittest.main()
