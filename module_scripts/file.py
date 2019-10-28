#!/usr/bin/env python3

import pprint
import os
import re

def file_set_permissions_chmod(history_file,cwd):

    # lines in the .bash_history file into an array, one element per line
    lines = [line.rstrip('\n') for line in open(history_file)]
    file_permission_lines = lines
    files_recurse = list()
    files = list()
    file_permissions = list()

    for i in list(file_permission_lines):
        if "chmod" not in i:
            file_permission_lines.remove(i)

    # array of words specific to apt and not a package
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


def file_set_permissions_chown(history_file,cwd):

    # lines in the .bash_history file into an array, one element per line
    lines = [line.rstrip('\n') for line in open(history_file)]
    file_permission_lines = lines
    files_recurse = list()
    files = list()
    file_users = list()
    file_groups = list()
    user_lines = list()

    for i in list(file_permission_lines):
        if "chown" not in i:
            file_permission_lines.remove(i)

    # array of words specific to apt and not a package
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





