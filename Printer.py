#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#########################################################################################################################
# Created on 01/20/2020 by Virag Doshi
# Copyright © 2020 Virag Doshi
#
#########################################################################################################################

isVerbose = False

def verbosePrinter(inStr):
    if isVerbose:
        print str(inStr)

def verboseAddition(inStr):
	return inStr if isVerbose else inStr