#!/usr/bin/env python3


def git_clone(history_file,cwd):

    # lines in the .bash_history file into an array, one element per line
    lines = [line.rstrip('\n') for line in open(history_file)]
    git_lines = lines
    repos = list()
    destionations = list()

    # remove elements with out "git clone"
    for i in list(git_lines):
        if "git clone" not in i:
            git_lines.remove(i)

    git_args = [ 'git', 'clone' ]

    # parse through every line
    for i in range(len(git_lines)):

        # array of words per each line
        line_args = git_lines[i].split()

        for j in range(len(line_args)):
            res = [ element for element in git_args if(element in line_args[j])]
            if "https" in line_args[j] or "ssh" in line_args[j]:
               repos.append(line_args[j])
            elif not res:
               destionations.append(line_args[j])

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")
    file_object.write("- name: clone needed git repos\n")
    file_object.write("  git:\n")
    file_object.write("    repo: \"{{ item.repo }}\"\n")
    file_object.write("    dest: \"{{ item.dest }}\"\n")
    file_object.write("    force: yes\n")
    file_object.write("  with_items:\n")
    
    for i in range(len(repos)):
        file_object.write("    - { src: \"" + repos[i] + "\", dest: \"" + destionations[i] + "\" }\n")

    file_object.write("\n")
    file_object.close()

