#!/usr/bin/env python3

from pprint import pprint

def apt(history_file,cwd):

    lines = [line.rstrip('\n') for line in open(history_file)]
    packages = list()

    apt_packages = lines

    for i in list(apt_packages):
        if "apt install" not in i and "apttitude install" not in i:
            apt_packages.remove(i)

    apt_args = [ 'apt', 'install', 'apttitude']

    for i in range(len(apt_packages)):
        line_args = apt_packages[i].split()

        for j in range(len(line_args)):
            res = [ element for element in apt_args if(element in line_args[j])]
            if not res:
                packages.append(line_args[j])

    history_file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")

    history_file_object.write("- name: install dependencies\n")
    history_file_object.write("  apt:\n")
    history_file_object.write("    name:\n")

    for i in range(len(packages)):
        history_file_object.write("      - " + packages[i] + "\n")

    history_file_object.write("    state: latest\n")
    history_file_object.write("\n")

    history_file_object.close()
