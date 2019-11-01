#!/usr/bin/env python3


def create_playbook(cwd):
    file_object = open(cwd + "/playbook/main.yml", "a+")


    file_object.write("---\n")
    file_object.write("\n")
    file_object.write("- hosts: server\n")
    file_object.write("  become: true\n")
    file_object.write("  gather_facts: no\n")
#    file_object.write("  vars_files:\n")
#    file_object.write("   - vars\n")
    file_object.write("  roles:\n")
    file_object.write("   - main\n")
    file_object.write("\n")
    file_object.write("...")
    file_object.close()

