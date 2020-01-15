#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#########################################################################################################################
# Created on 01/16/2020 by Virag Doshi
# Copyright © 2020 Virag Doshi
#
#########################################################################################################################

import sys
import argparse
import textwrap
import json
import os
import Printer
import shutil
import re
import base64
from Riddler import *


welcomeString = """
GoTHa: Gota group's Treasure Hunt
 ______________________
< Hi, welcome to GoTHa >
 ----------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||

There are a few locked puzzles in this repo. To open the envelopes that contain your gifts, \
you will have to solve them. This script is the key to verify if the answers you come up with \
for the puzzles are right or wrong.

There is one puzzle each for each of the eight envelopes. After solving puzzle number n, you may \
open the nth envelope. Only when you submit to the script the correct answer to the current puzzle, \
will the question for the next one appear.

Note:
* Please do not alter the contents of the folder resources/data. Doing so may render the scripts \
inoperable. 
* The unlocked puzzles can be found in resources/puzzles in a directory named with the level number.

When you are ready, head over to resources/puzzles and find the first puzzle to get started. \
Best of luck!

How to use this script:
"""

def create(createInputDir, encDir, decDir):
    with open(os.path.join(createInputDir, 'input.json'),'r') as fIn:
        inputDict = json.loads(fIn.read())

    level = 1
    prevKey = None
    outputDict = { }

    assert ('1' in inputDict), "First level not found"

    print "Copying level 1 files to puzzles"

    if os.path.exists(os.path.join(decDir, '1')):
        shutil.rmtree(os.path.join(decDir, '1'))

    shutil.copytree(os.path.join(createInputDir, '1'), os.path.join(decDir, '1'))

    while 1:
        print "Found level " + str(level) + \
               Printer.verboseAddition(": " + str(inputDict[str(level)]))
        Printer.verbosePrinter("Generating dictionary")
        riddler                 = Riddler(level, inputDict[str(level)], prevKey)
        levelDict               = riddler.getEncDict()
        Printer.verbosePrinter("Created dictionary: " + str(levelDict))
        outputDict[str(level)]  = levelDict
        prevKey                 = riddler.getNextKey()
        level += 1
        print
        if str(level) not in inputDict:
            break
        print "Encrypting level " + str(level) + " files"
        riddler.encryptNextFiles()

    with open(os.path.join(encDir, 'enc.json'), 'w') as fOut:
        json.dump(outputDict, fOut)


def solve(inLevel, inAnswer, encDir, decDir):
    with open(os.path.join(encDir, 'enc.json'),'r') as fIn:
        inputDict = json.loads(fIn.read())

    if str(inLevel) not in inputDict:
        print "No such level found"
        exit(-1)

    print "Found level " + str(inLevel) + \
               Printer.verboseAddition(": " + str(inputDict[str(inLevel)]))
    solver = Solver(inLevel, inputDict[str(inLevel)])

    if solver.isAnswerCorrect(inAnswer):
        print "Correct answer given"
    else:
        print "Incorrect answer given"
        exit(-1)

    if str(inLevel + 1) not in inputDict:
        print "Congrats! You have solved all the puzzles"
        return

    solver.decryptNextFiles(inAnswer)

    print "Decrypting level " + str(inLevel + 1) + " files"
    print "Resulting files can be found at " + solver.outDir


def saltDecryptor(inLevel, inPrevAnswer, encDir):
    with open(os.path.join(encDir, 'enc.json'),'r') as fIn:
        inputDict = json.loads(fIn.read())

    if str(inLevel) not in inputDict:
        print "No such level found"
        exit(-1)

    print "Found level " + str(inLevel) + \
               Printer.verboseAddition(": " + str(inputDict[str(inLevel)]))

    print "Decrypting salt for level " + str(inLevel)
    salt    = base64.urlsafe_b64decode(str(inputDict[str(inLevel)]['salt']))
    pepper  = Solver.decryptSalt(salt, None if inLevel is 1 else inPrevAnswer)

    print "Pepper found: " + pepper


def main():
    parser = argparse.ArgumentParser(description = "GoTHa: Gota group's Treasure Hunt")
    parser.add_argument('action', metavar = 'action', nargs = '?', 
                        help = 'Create or solve puzzles')
    parser.add_argument('level', metavar = 'level', nargs = '?', 
                        help = 'Level to be solved')
    parser.add_argument('answer', metavar = 'answer', nargs = '?', 
                        help = 'Answer to the level to be solved. It is case insensitive. '
                        'It should contain no spaces and only alphanumeric '
                        'chatacters. For example "this answer" would become "thisanswer"')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action='store_true',
                        help = "Verbose")
    args = parser.parse_args()

    Printer.isVerbose = args.verbose

    resourceDir         = 'resources'
    createInputDir      = os.path.join(resourceDir, 'inputs')
    encDir              = os.path.join(resourceDir, 'data')
    decDir              = os.path.join(resourceDir, 'puzzles')

    Riddler.inputDir    = createInputDir
    Riddler.outputDir   = encDir

    Solver.inputDir     = encDir
    Solver.outputDir    = decDir

    if args.action is None:
        print welcomeString
        print parser.print_help()
        exit(0)

    if args.action not in ['solve', 'create', 'pepper']:
        print "Invalid action"
        print parser.print_help(sys.stderr)
        exit(-1)

    if args.action == 'solve' or args.action == 'pepper':
        try:
            level = int(args.level)
        except (TypeError, ValueError) as e:
            print "Invalid level"
            print parser.print_help(sys.stderr)
            exit(-1)
        if (args.answer is None) and \
            ((args.action == 'solve') or \
             (args.action == 'pepper' and level is not 1)):
            print "No answer given"
            print parser.print_help(sys.stderr)
            exit(-1)
        answer = re.sub('[^A-Za-z0-9]+', '', str(args.answer))

        if args.action == 'solve':
            solve(level, answer, encDir, decDir)
        else:
            saltDecryptor(level, answer, encDir)

    if args.action == 'create':
        if args.level is not None:
            print "Creation cannot take a level number"
            print parser.print_help(sys.stderr)
            exit(-1)

        create(createInputDir, encDir, decDir)


if __name__ == '__main__':
    main()
