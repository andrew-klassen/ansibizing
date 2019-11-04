#!/usr/bin/env python3


import copy
import subprocess
import os
from os.path import expanduser

# function return current path at the time for a given line number
def current_directory(lines, line_number):
    
    directory_lines = copy.deepcopy(lines)
    
    # script assumes that the users home directory was the starting point if no begining absolute path was provided
    current_path = expanduser("~")

    # itterate through every line
    for i in range(line_number):
        
        # safety for when range is larger than size
        if i >= len(directory_lines):
            break

        # skip itteration if line has no cd
        if "cd " not in directory_lines[i]:
            continue

        line_args = directory_lines[i].split()

        # if absolute path was provided
        if '/' in line_args[1][0]:
            current_path = line_args[1]
        else:
            current_path = current_path + '/' + line_args[1]
        
        # resolves all '..' is the current path has any
        if '..' in current_path:
            directories = current_path.split('/')

            # when split first element would always be empty because full path start with /
            del directories[0]

            count = 0

            for j in list(directories):
                if '..' == j:
                    
                    # remove '..' element and the one behind it
                    temp = directories[count - 1]
                    directories.remove(temp)
                    directories.remove(j)
                    count -= 2
                count += 1
            current_path = ""

            # merge elements back together
            for j in range(len(directories)):
                current_path = current_path + '/' + directories[j]
    
    return current_path

# returns the line number of a provided line
def locate_line (lines, line):

    for i in range(len(lines)):
        if line in lines[i]:
            return i + 1

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files or name in dirs:
            return os.path.join(root, name)


def prep(cwd):
    print("test")    

