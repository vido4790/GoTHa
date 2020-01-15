#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#########################################################################################################################
# Created on 01/15/2020 by Virag Doshi
# Copyright © 2020 Virag Doshi
#
#########################################################################################################################

import unittest, random
import Crypto, Tar, Riddler

if __name__ == '__main__':
    random.seed()
    testsuite = unittest.TestLoader().discover('.', pattern = '*.py')
    unittest.TextTestRunner(verbosity=1).run(testsuite)
