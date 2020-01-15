#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#########################################################################################################################
# Created on 01/14/2020 by Virag Doshi
# Copyright © 2020 Virag Doshi
#
#########################################################################################################################

import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import unittest, random


class HashSuite(object):
    @staticmethod
    def hash(inStr, inSalt):
        salt    = 'A\r\xbc\x05\xed0\x07\x01\xb2VZ\xe8\xd0\x17\x88\xa8\x93z\xbe\xb0Sk\xee\x90b\x80D@e\xa8g\x07'
        digest  = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(inStr + salt + inSalt)
        return digest.finalize()


class CipherSuite(object):
    def __init__(self, inKey):
        keyDerivator    = PBKDF2HMAC(algorithm = hashes.SHA256(), length = 32,
                                     salt = b'4\xe8\xf3W\xbb\x8e\xbe\xe8\xebl\x1f&\xf4T\x1b\xe2', 
                                     iterations = 100000,  backend = default_backend())
        key             = base64.urlsafe_b64encode(keyDerivator.derive(inKey))
        # https://github.com/fernet/spec/blob/master/Spec.md
        self.fernet     = Fernet(key)   # AES-128 CBC, HMAC-256

    def encrypt(self, inBytes):
        return self.fernet.encrypt(inBytes)

    def decrypt(self, inBytes):
        return self.fernet.decrypt(inBytes)

    def _operate(self, inFile, outFile, inOperation):
        with open(inFile, 'r') as fIn:
            dataIn = fIn.read()

        dataOut = inOperation(dataIn)

        with open(outFile, 'w') as fOut:
            fOut.write(dataOut)

    def encryptFile(self, inFile, outFile):
        self._operate(inFile, outFile, self.encrypt)

    def decryptFile(self, inFile, outFile):
        self._operate(inFile, outFile, self.decrypt)



#########################################################################################################################
# Testing
#########################################################################################################################


class _EncryptDecryptTests(unittest.TestCase):
    def testStringEnc(self):
        for i in range(100):
            keySize         = random.randint(0, 128)
            key             = os.urandom(keySize)

            inputStrSize    = random.randint(0, 1024)
            inputStr        = os.urandom(inputStrSize)
            
            cipherSuite     = CipherSuite(key)
            enc             = cipherSuite.encrypt(inputStr)

            cipherSuite     = CipherSuite(key)
            dec             = cipherSuite.decrypt(enc)
            
            self.assertEqual(dec, inputStr)

    def testFileEnc(self):
        for i in range(100):
            keySize         = random.randint(0, 128)
            key             = os.urandom(keySize)

            inputFileSize   = random.randint(0, 1024)
            inputStr        = os.urandom(inputFileSize)

            inputFile       = '/tmp/testIn.txt'
            encFile         = '/tmp/testIn.enc'
            decFile         = '/tmp/testOut.txt'

            with open(inputFile, 'w') as fIn:
                fIn.write(inputStr)

            cipherSuite     = CipherSuite(key)
            cipherSuite.encryptFile(inputFile, encFile)

            cipherSuite     = CipherSuite(key)
            cipherSuite.decryptFile(encFile, decFile)

            with open(inputFile, 'r') as fIn:
                with open(decFile, 'r') as fOut:
                    self.assertEqual(fIn.read(), fOut.read())


class _HashingTests(unittest.TestCase):
    def testHashing(self):
        for i in range(100):
            saltSize        = random.randint(0, 128)
            salt            = os.urandom(saltSize)

            inputStrSize    = random.randint(0, 1024)
            inputStr        = os.urandom(inputStrSize)
        
            self.assertEqual(HashSuite.hash(inputStr, salt), HashSuite.hash(inputStr, salt))


if __name__ == '__main__':
    random.seed()
    unittest.main()
