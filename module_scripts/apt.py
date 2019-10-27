#!/usr/bin/env python3


def apt(history_file,cwd):

    # lines in the .bash_history file into an array, one element per line
    lines = [line.rstrip('\n') for line in open(history_file)]
    packages = list()
    apt_packages = lines

    # remove non apt elements"
    for i in list(apt_packages):
        if "apt install" not in i and "apttitude install" not in i:
            apt_packages.remove(i)

    # array of words specific to apt and not a package
    apt_args = [ 'apt', 'install', 'apttitude']

    # parse through every line
    for i in range(len(apt_packages)):
        line_args = apt_packages[i].split()

        for j in range(len(line_args)):
            res = [ element for element in apt_args if(element in line_args[j])]
            if not res:
                packages.append(line_args[j])

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")
    file_object.write("- name: install dependencies\n")
    file_object.write("  apt:\n")
    file_object.write("    name:\n")

    for i in range(len(packages)):
        file_object.write("      - " + packages[i] + "\n")

    file_object.write("    state: latest\n")
    file_object.write("\n")
    file_object.close()

