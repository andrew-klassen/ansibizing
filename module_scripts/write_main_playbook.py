#!/usr/bin/env python3


def creat_playbook(cwd)
    history_file_object = open(cwd + "/playbook/main.yml", "a+")

    history_file_object.write("- hosts: servers\n")
    history_file_object.write("  become: true\n")
    history_file_object.write("  gather_facts: no\n")
    history_file_object.write("  vars_files:\n")
    history_file_object.write("   - vars\n")
    history_file_object.write("  roles:\n")
    history_file_object.write("   - main\n")

    history_file_object.close()

