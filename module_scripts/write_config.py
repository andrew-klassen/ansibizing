#!/usr/bin/env python3


def create_config(cwd):
    file_object = open(cwd + "/playbook/ansible.cfg", "a+")

    file_object.write("[defaults]\n")
    file_object.write("inventory = hosts\n")
    file_object.write("interpreter_python = /usr/bin/python3\n")
    file_object.write("host_key_checking = False\n")
    file_object.write("remote_tmp = /tmp/.ansible-${USER}/tmp\n")

    file_object.close()
