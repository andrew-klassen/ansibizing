#!/usr/bin/env python3


import copy
import subprocess
import os
import shutil
import requests
import pprint
from os.path import expanduser

def mysql_filter(mysql_lines):

    try:
        mysql_lines.remove("_HiStOrY_V2_")
    except:
        pass

    while "exit;" in mysql_lines: 
        mysql_lines.remove("exit;")

    for i in range(len(mysql_lines)):
        mysql_lines[i] = mysql_lines[i].replace("\\040", " ")
    
    return mysql_lines

def set_history(cwd, user):

    # user is assumed to be root if no user is provided
    history_file = "/root"
    mysql_history_file = "/root"


    if user is not None and user != "root":
        history_file = find(user,"/home")
        history_file = history_file + "/.bash_history"

        mysql_history_file = find(user,"/home")
        mysql_history_file = mysql_history_file + "/.mysql_history"

    else:
        history_file = history_file + "/.bash_history"
        mysql_history_file = mysql_history_file + "/.mysql_history"

    # set lines array
    if os.path.isfile(cwd + "/playbook/history_files/prep"):
        lines = [line.rstrip('\n') for line in open(cwd + "/playbook/history_files/prep")]
    else:
        lines = [line.rstrip('\n') for line in open(history_file)]
        if os.path.isfile(mysql_history_file):
            mysql_lines = [line.rstrip('\n') for line in open(mysql_history_file)]
            mysql_lines = mysql_filter(mysql_lines)
            #pprint(mysql_lines)
            lines.extend(mysql_lines)

    # copies of history files are archived in case the user needs to reverse engineer
    shutil.copyfile(history_file, cwd + "/playbook/history_files/bash_history")
    if os.path.isfile(mysql_history_file):
            shutil.copyfile(mysql_history_file, cwd + "/playbook/history_files/mysql_history")

    return lines


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


def prep(cwd, user):

    # lines will equal the prep file if it exists, if not .bash_history
    lines = set_history(cwd, user) 

    # end function if prep was used
    if os.path.isfile(cwd + "/playbook/history_files/prep"):
        return lines

    filtered_lines = list()

    file_object = open(cwd + "/playbook/history_files/prep", "a+")
    

    for i in range(len(lines)):

        # used to continue outer loop from inner
        skip = False
        line_args = lines[i].split()

        # if line is empty
        if not lines[i]:
            continue

        # cd commands to directories that don't exist
        elif line_args[0] == "cd":

            if line_args[1].startswith("/"):
                if not os.path.isdir(line_args[1]):
                    continue
            else:
                if not os.path.isdir(current_directory(lines, i + 1)):
                    continue
        
        for j in range(len(line_args)):

            # make sure links in history are not broken
            if line_args[j].startswith("http"):
               
               try:
                   request = requests.get(line_args[j])
               except:
                   skip = True

               if not request.status_code == 200:
                   skip = True
        
        if skip:
            continue

        filtered_lines.append(lines[i])
        file_object.write(lines[i] + "\n")
   
    file_object.close()

    return filtered_lines

