#!/usr/bin/env python3


import copy


def apt_key_add(lines,cwd):

    apt_key_lines = copy.deepcopy(lines)
    apt_keys_url = list()
    apt_keys_keyserver = list()
    apt_keys_id = list()

    # remove non ppa elements
    for i in list(apt_key_lines):
        if "apt-key" not in i:
            apt_key_lines.remove(i)

    # end function if apt-key was not used
    if not apt_key_lines:
        return None


    for i in range(len(apt_key_lines)):
        line_args = apt_key_lines[i].split()

        for j in range(len(line_args)):
            if line_args[j].startswith("http"):
                apt_keys_url.append(line_args[j])
            elif line_args[j] == "--keyserver":
                apt_keys_keyserver.append(line_args[j + 1])
            elif line_args[j] == "--recv-keys":
                apt_keys_id.append(line_args[j + 1])


    # remove duplicate urls
    apt_keys_url = list(dict.fromkeys(apt_keys_url))

    # add gpg keys added by url
    if apt_keys_url:

        file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")

        file_object.write("- name: add gpg keys by url\n")
        file_object.write("  apt_key:\n")
        file_object.write("    url: \"{{ item }}\"\n")
        file_object.write("  with_items:\n")

        for i in range(len(apt_keys_url)):
            file_object.write("    - " + apt_keys_url[i] + "\n")

        file_object.write("\n")

    # add gpg keys by keyserver
    if apt_key_keyserver:

        file_object.write("- name: add gpg keys by keyserver and id\n")
        file_object.write("  apt_key:\n")
        file_object.write("    keyserver: \"{{ item.keyserver }}\"\n")
        file_object.write("    id: \"{{ item.id }}\"\n")
        file_object.write("  with_items:\n")

        for i in range(len(apt_keys_keyserver)):
            file_object.write("    - { keyserver: \"" + apt_keys_keyserver[i] + "\", id: \"" + apt_keys_id[i] + "\" }\n")

        file_object.write("\n")


    file_object.close()


def ppa_add(lines,cwd):

    ppa_lines = copy.deepcopy(lines)
    ppas = list()
    
    # remove non ppa elements
    for i in list(ppa_lines):
        if "add-apt-repository" not in i:
            ppa_lines.remove(i)

    if not ppa_lines:
        return None

    ppa_args = [ 'add-apt-repository' ]

    for i in range(len(ppa_lines)):
        line_args = ppa_lines[i].split()

        for j in range(len(line_args)):
            res = [ element for element in ppa_args if(element in line_args[j])]
            if not res:
                ppas.append(line_args[j])
    
    # remove duplicate packages
    ppas = list(dict.fromkeys(ppas))

    file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")
    file_object.write("- name: add the following ppas\n")
    file_object.write("  apt_repository:\n")
    file_object.write("    repo: \"{{ item }}\"\n")
    file_object.write("  with_items:\n")

    for i in range(len(ppas)):
        file_object.write("    - " + ppas[i] + "\n")

    file_object.write("\n")

    file_object.close()


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

