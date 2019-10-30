#!/usr/bin/env python3


def create_hosts(cwd):
    file_object = open(cwd + "/playbook/hosts", "a+")

    file_object.write("[server]\n")
    file_object.write("127.0.0.1\n")

    file_object.close()

