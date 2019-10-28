#!/usr/bin/env python3

import pprint

def file_set_permissions_chmod(history_file,cwd):

    # lines in the .bash_history file into an array, one element per line
    lines = [line.rstrip('\n') for line in open(history_file)]
    file_permission_lines = lines
    files_recurse = list()
    files = list()

    for i in list(file_permission_lines):
        if "chmod" not in i:
            file_permission_lines.remove(i)

    # array of words specific to apt and not a package
    chmod_args = [ 'chmod', '-R']

    recurse = False
    # parse through every line
    for i in range(len(file_permission_lines)):
        line_args = file_permission_lines[i].split()

        for j in range(len(line_args)):

            if line_args[j].isdigit():
                continue
            elif "-R" in line_args[j]:
                recurse = True
                
            res = [ element for element in chmod_args if(element in line_args[j])]
            if not res:
                files.append(line_args[j])
                files_recurse.append(recurse)

    pprint.pprint(files)
    pprint.pprint(files_recurse)

                
    

