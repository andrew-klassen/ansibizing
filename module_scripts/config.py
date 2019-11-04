#!/usr/bin/env python3


import os
from .general_functions import *

cwd = os.getcwd()

def set_history(user):

    history_file = "/root"

    if user is not None:
        history_file = find(user,"/home")
        history_file = history_file + "/.bash_history"

    # lines in the .bash_history file into an array, one element per line
    lines = [line.rstrip('\n') for line in open(history_file)]
    
    return lines

