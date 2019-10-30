#!/usr/bin/env python3


import copy

def apt(lines,cwd):

    packages = list()
    apt_packages = copy.deepcopy(lines)

    # remove non apt elements
    for i in list(apt_packages):
        if "apt install" not in i and "apttitude install" not in i:
            apt_packages.remove(i)

    # end function if apt is not used
    if not apt_packages:
        return None

    # array of words specific to apt and not a package
    apt_args = [ 'apt', 'install', 'apttitude']

    # parse through every line
    for i in range(len(apt_packages)):
        line_args = apt_packages[i].split()

        for j in range(len(line_args)):
            res = [ element for element in apt_args if(element in line_args[j])]
            if not res:
                packages.append(line_args[j])

    # remove duplicate packages
    packages = list(dict.fromkeys(packages))

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")
    file_object.write("- name: update apt cache\n")
    file_object.write("  apt:\n")
    file_object.write("    update_cache: yes\n")
    file_object.write("    cache_valid_time: 3600\n")
    file_object.write("\n")

    file_object.write("- name: install dependencies\n")
    file_object.write("  apt:\n")
    file_object.write("    name:\n")

    for i in range(len(packages)):
        file_object.write("      - " + packages[i] + "\n")

    file_object.write("    state: latest\n")
    file_object.write("\n")
    file_object.close()

