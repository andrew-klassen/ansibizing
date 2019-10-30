#!/usr/bin/env python3


import os

cwd = os.getcwd()
history_file = "/home/applebyco.com/aklassenadmin/.bash_history"

# lines in the .bash_history file into an array, one element per line
lines = [line.rstrip('\n') for line in open(history_file)]

