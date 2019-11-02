#!/usr/bin/env python3


import copy
import pprint
from .general_functions import *

def tar(lines,cwd):
    
    tar_lines = copy.deepcopy(lines)
    unarchive_source = list()
    unarchive_destination = list()

    # get list of tar only commands to make sure tar is used 
    for i in list(tar_lines):
        if "tar" not in i:
            tar_lines.remove(i)

    # end function if 
    if not tar_lines:
        return None

    # list of tar specific arguments
    tar_args = [ 'tar' ]

    for i in range(len(lines)):
        line_args = lines[i].split()

        for j in range(len(line_args)):
            res = [ element for element in tar_args if(element in line_args[j])]

            # set values if index is with in range
            try:
                previous_argument = line_args[j - 1]
            except:
                previous_argument = ""

            try:
                second_arg = line_args[1]
            except:
                second_arg = ""

            if not res:

                if ("C" in previous_argument or "--directory" in previous_argument) and previous_argument.startswith('-'):
                    unarchive_destination.append(line_args[j])
                    unarchive_source.append(line_args[2])
                if "x" in second_arg and "x" in previous_argument:
                    unarchive_source.append(line_args[j])
                    unarchive_destination.append(current_directory(lines,i + 1))

