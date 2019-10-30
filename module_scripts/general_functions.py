#!/usr/bin/env python3


import copy
import pprint
from os.path import expanduser

def current_directory(lines, line_number):
    
    directory_lines = copy.deepcopy(lines)

    current_path = expanduser("~")
    for i in range(line_number):
        
        # safety for when range is larger than size
        if i >= len(directory_lines):
            break

        if "cd " not in directory_lines[i]:
            continue

        line_args = directory_lines[i].split()

        if '/' in line_args[1][0]:
            current_path = line_args[1]
        else:
            current_path = current_path + '/' + line_args[1]

        if '..' in current_path:
            directories = current_path.split('/')
            del directories[0]
            count = 0
            for j in list(directories):
                if '..' == j:
                    temp = directories[count - 1]
                    directories.remove(temp)
                    directories.remove(j)
                    count -= 2
                count += 1
            current_path = ""
            for j in range(len(directories)):
                current_path = current_path + '/' + directories[j]
    
    return current_path
