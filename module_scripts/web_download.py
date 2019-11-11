#!/usr/bin/env python3


import copy
from .general_functions import *


def wget(lines,cwd):
    
    wget_lines = copy.deepcopy(lines)
    locations = list()
    location_directories = list()

    for i in list(wget_lines):
        if "wget" not in i:
            wget_lines.remove(i)

    # end function if wget is not used
    if not wget_lines:
        return None

    # array of words specific to apt and not a package
    wget_args = [ 'wget' ]

    # parse through every line
    for i in range(len(lines)):
        line_args = lines[i].split()

        for j in range(len(line_args)):
            res = [ element for element in wget_args if(element in line_args[j])]
            if not res and "http" in line_args[j] and "wget" in lines[i]:
                locations.append(line_args[j])
                location_directories.append(current_directory(lines, i + 1))

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")
    file_object.write("- name: download files from wget\n")
    file_object.write("  get_url:\n")
    file_object.write("    url: \"{{ item.url }}\"\n")
    file_object.write("    dest: \"{{ item.dest }}\"\n")
    file_object.write("  with_items:\n")

    for i in range(len(locations)):
        file_object.write("    - { url: \"" + locations[i] + "\", dest: \"" + location_directories[i] + "\" }\n")

    file_object.write("\n")
    file_object.close()



def curl(lines,cwd):

    curl_lines = copy.deepcopy(lines)
    locations = list()
    location_directories = list()

    for i in list(curl_lines):
        if "curl " not in i:
            curl_lines.remove(i)

    # end function if wget is not used
    if not curl_lines:
        return None

    # array of words specific to apt and not a package
    curl_args = [ 'curl' ]

    # parse through every line
    for i in range(len(lines)):
        line_args = lines[i].split()

        for j in range(len(line_args)):
            res = [ element for element in curl_args if(element in line_args[j])]
            if not res and "http" in line_args[j] and "curl" in lines[i]:
                locations.append(line_args[j])
                location_directories.append(current_directory(lines, i + 1))

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")
    file_object.write("- name: download files from curl\n")
    file_object.write("  get_url:\n")
    file_object.write("    url: \"{{ item.url }}\"\n")
    file_object.write("    dest: \"{{ item.dest }}\"\n")
    file_object.write("  with_items:\n")

    for i in range(len(locations)):
        file_object.write("    - { url: \"" + locations[i] + "\", dest: \"" + location_directories[i] + "\" }\n")

    file_object.write("\n")
    file_object.close()

