#!/usr/bin/env python3


import os
import re
import copy

def file_set_permissions_chmod(lines,cwd):

    file_permission_lines = copy.deepcopy(lines)

    # boolean array, if chmod was recursive
    files_recurse = list()
    files = list()

    # numerical form of chmod permissions 
    file_permissions = list()

    for i in list(file_permission_lines):
        if "chmod" not in i:
            file_permission_lines.remove(i)

    # exit if no chmod
    if not file_permission_lines:
        return None

    # array of arguments specific to chmod
    chmod_args = [ 'chmod', "-R" ]

    # parse through every line

    for i in range(len(file_permission_lines)):
        line_args = file_permission_lines[i].split()

        recurse = False
        for j in range(len(line_args)):

            if line_args[j].isdigit():
                file_permissions.append(line_args[j])
                continue

            elif "-R" in line_args[j]:
                recurse = True
                
            res = [ element for element in chmod_args if(element in line_args[j])]
            if not res:
                files.append(line_args[j])

        files_recurse.append(recurse)

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")

    for i in range(len(files)):

        file_object.write("- name: set file permissions (" + files[i] + ") \n")
        file_object.write("  file:\n")
        file_object.write("    path: " + files[i] + "\n")
        file_object.write("    mode: " + file_permissions[i] + "\n")
        
        if files_recurse[i]:
            file_object.write("    recurse: yes\n")

        if os.path.isdir(files[i]):
            file_object.write("    state: directory\n")
        
        file_object.write("\n")

    file_object.close()


def file_set_permissions_chown(lines,cwd):

    file_permission_lines = copy.deepcopy(lines)
    files_recurse = list()
    files = list()
    file_users = list()
    file_groups = list()
    user_lines = list()

    for i in list(file_permission_lines):
        if "chown" not in i:
            file_permission_lines.remove(i)

    if not file_permission_lines:
        return None

    # array of words specific to chown
    chmod_args = [ 'chown', "-R" ]

    # parse through every line
    for i in range(len(file_permission_lines)):
        line_args = file_permission_lines[i].split()

        recurse = False
        for j in range(len(line_args)):

            if "." in line_args[j] or ":" in line_args[j]:
                argument = re.split("[.:]", line_args[j])
                user = argument[0]
                group = argument[1]
                user_lines = [line.rstrip('\n') for line in open("/etc/shadow")] 
                for k in range(len(user_lines)):
                    if user in user_lines[k]:
                        file_users.append(user)
                        file_groups.append(group)
                        break;

                continue
            elif "-R" in line_args[j]:
                recurse = True
                
            res = [ element for element in chmod_args if(element in line_args[j])]
            if not res:
                files.append(line_args[j])

        files_recurse.append(recurse)

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")

    for i in range(len(files)):

        file_object.write("- name: set file ownership (" + files[i] + ") \n")
        file_object.write("  file:\n")
        file_object.write("    path: " + files[i] + "\n")
        file_object.write("    owner: " + file_users[i] + "\n")
        file_object.write("    group: " + file_groups[i] + "\n")

        if files_recurse[i]:
            file_object.write("    recurse: yes\n")

        if os.path.isdir(files[i]):
            file_object.write("    state: directory\n")

        file_object.write("\n")

    file_object.close()


def mkdir():
    mkdir_lines = copy.deepcopy(lines)

    # remove non mkdir lines
    for i in list(mkdir_lines):
        if "mkdir " not in i:
            mkdir_lines.remove(i)

    if not apt_packages:
        return None













