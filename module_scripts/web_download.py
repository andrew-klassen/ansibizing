#!/usr/bin/env python3


import pprint

def wget(lines,cwd):
    
    wget_lines = lines
    locations = list()

    for i in list(wget_lines):
        if "wget" not in i:
            wget_lines.remove(i)

    # end function if wget is not used
    if not wget_lines:
        return None

    # array of words specific to apt and not a package
    wget_args = [ 'wget' ]

    # parse through every line
    for i in range(len(wget_lines)):
        line_args = wget_lines[i].split()

        for j in range(len(line_args)):
            res = [ element for element in wget_args if(element in line_args[j])]
            if not res and "http" in line_args[j]:
                locations.append(line_args[j])

    # remove duplicate locations
    locations = list(dict.fromkeys(locations))

    pprint.pprint(locations)
