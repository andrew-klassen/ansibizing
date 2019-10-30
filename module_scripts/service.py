#!/usr/bin/env python3


import copy

def service_systemctl(lines,cwd):

    service_names = list()
    service_lines = copy.deepcopy(lines)

    # remove non systemctl lines
    for i in list(service_lines):
        if "systemctl" not in i or "status" in i:
            service_lines.remove(i)

    for i in range(len(service_lines)):
        line_args = service_lines[i].split()
        temp = line_args[-1]
        temp = temp.replace(".service","")
        service_names.append(temp)

    # boolean flags for loop
    enable_found = False
    disable_found = False

    for i in range(len(service_names)):
        for j in range(len(service_lines)):
            if service_names[i] in service_lines[j] and "enable" in service_lines[j]:
                enable_found = True
                break
            elif service_names[i] in service_lines[j] and "disable" in service_lines[j]:
                disable_found = True
                break

        playbook_lines = [line.rstrip('\n') for line in open(cwd + "/playbook/roles/main/tasks/main.yml")]
        service_exists = False
        for j in range(len(playbook_lines)):
            if service_names[i] in playbook_lines[j]:
                service_exists = True
                break

        if service_exists:
            continue

        # write to playbook, playbook is read each type to check and see if service was already added
        file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")

        file_object.write("- name: service " + service_names[i] +"\n")
        file_object.write("  service:\n")
        file_object.write("    name: " + service_names[i] + "\n")

        if enable_found:
            file_object.write("    state: restarted\n")
            file_object.write("    enabled: yes\n")
            enable_found = False
        elif disable_found:
            file_object.write("    state: stopped\n")
            file_object.write("    enabled: no\n")
            enable_found = False
        else:
            file_object.write("    state: restarted\n")

        file_object.write("\n")
        file_object.close()

