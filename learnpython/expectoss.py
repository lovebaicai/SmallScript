#!/usr/bin/env python

import sys
import paramiko

def sshclient(ip, username, password, cmd):

    myclient = paramiko.SSHClient()

    myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    myclient.connect(ip, port=22, username=username, password=password, timeout=5)

    stdin, stdout, stderr = myclient.exec_command(cmd)

    stdin.write("y\n")

    print stdout.readlines()

    myclient.close()



cmd = 'python /home//do.py'

sshclient('hostname', 'username', 'password', cmd=cmd)
