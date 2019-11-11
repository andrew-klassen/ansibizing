#!/usr/bin/env python3


import shutil
import copy


def copy_config(lines,cwd):

    files = list()
    file_changes = copy.deepcopy(lines)

    text_editor_args = [ 'vim', 'nano', 'emacs']

    # remove elements that have nothing to do with a text editor
    for i in list(file_changes):
        res = [ element for element in text_editor_args if(element in i)]
        if not res:
            file_changes.remove(i)

    if not file_changes:
        return None

    # parse through every line
    for i in range(len(file_changes)):
        line_args = file_changes[i].split()

        for j in range(len(line_args)):
            res = [ element for element in text_editor_args if(element in line_args[j])]
            if not res:
                files.append(line_args[j])

    
    filenames = list()

    for i in range(len(files)):
        temp = files[i].split('/')
        filename = temp[-1]
        filenames.append(filename)
        shutil.copyfile(files[i], cwd + "/playbook/source/" + filename)

    # write to playbook
    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")
    file_object.write("- name: copy all config files\n")
    file_object.write("  copy:\n")
    file_object.write("    src: \"{{ item.src }}\"\n")
    file_object.write("    dest: \"{{ item.dest }}\"\n")
    file_object.write("  with_items:\n")

    for i in range(len(files)):
        file_object.write("    - { src: \"source/" + filenames[i] + "\", dest: \"" + files[i] + "\" }\n")

    file_object.write("\n")
    file_object.close()

