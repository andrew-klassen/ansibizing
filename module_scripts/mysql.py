#!/usr/bin/env python3


import copy
import mysql.connector
import os


# this module uses an array of objects (user_objects) to store atributes about each user that was created
class user_object:

    def __init__(self, username, host, password = None, grants = None, database_and_table = None, grant_option = False):
        
        self.__username = username
        self.__host = host
        self.__password = password
        self.__grants = grants
        self.__database_and_table = database_and_table

        if self.__database_and_table:
            self.__database_and_table = self.__database_and_table.replace(" ","")

        self.__grant_option = grant_option

    # prints the playbook for user
    def get_playbook_module(self):

        return_string = "- name: create \"" + self.__username + "\" user" + "\n"
        return_string += "  mysql_user:" + "\n"
        return_string += "    name: " + self.__username + "\n"

        # password, skips if user dosen't have a password
        #
        # password is always written to the playbook in hashed form 

        if self.__password == "" or self.__password is None:
            return_string += "    password: \"\"" + "\n"
        else:
            return_string += "    password: \"" + self.__password + "\"" + "\n"

        if self.__database_and_table and self.__grants:
            return_string += "    priv:  \"" + self.__database_and_table + ":" + "" + self.__grants + "\"" + "\n"
        
        return_string += "    state: present" + "\n" + "\n"

        return return_string

def mysql_users(lines,cwd):
    
    # root password authentication is temporary changed to allow python to connect to mysql instance as root
    result = os.system("mysql -u root -e \"ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';\" 2> /dev/null")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mysql"
    )

    # reads from the mysql users table, default users are excluded
    mycursor = mydb.cursor()
    mycursor.execute("SELECT user,host,authentication_string FROM mysql.user WHERE user != 'root' AND user != 'mysql.session' AND user != 'mysql.sys' AND user != 'debian-sys-maint';")
    users = mycursor.fetchall()

    # grant lines are lines from the prep file that contain grants for the user
    grant_lines = copy.deepcopy(lines)

    for i in list(grant_lines):
        if not i.lower().startswith("grant"):
            grant_lines.remove(i)

    users_class_array = list()

    # iterate through all the users gathered from mysql, purpose is to associate users with their grants and add them to the user_class_array
    for i in range(len(users)):

        username = users[i][0]
        host = users[i][1]
        password = users[i][2]
        grants = None

        for i in range(len(grant_lines)):
            
            if username in grant_lines[i] and host in grant_lines[i]:
                grant_words = grant_lines[i].split()
                on_index = 0
                to_index = 0

                # grant example, GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost' with grant option; 
                for j in range(len(grant_words)):
                    
                    # grants always come before key word "ON"
                    if grant_words[j].lower() == "on":
                        on_index = j
                        grants = " ".join(grant_words[1:on_index])

                    # grants always come before key word "ON"
                    elif grant_words[j].lower() == "to":
                        to_index = j
                        database_and_table = " ".join(grant_words[(on_index + 1):to_index])

        user = user_object(username,host,password,grants,database_and_table)
        users_class_array.append(user)

        # write to playbook
        file_object = open(cwd + "/playbook/roles/main/tasks/main.yml", "a+")

        if user.get_playbook_module() != None:
            file_object.write(user.get_playbook_module())

