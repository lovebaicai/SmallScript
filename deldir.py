#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: nemo_chen

import os
import shutil
import time
import datetime

path = os.path.dirname(os.path.abspath(__file__)) #deploy_uat_trunk_ent/modules/*

dirlist = os.listdir(path)

for dir in dirlist:
    if os.path.isdir(os.path.join(path, dir)):
        filedir = os.path.join(path, dir, 'builds')
        timelist = []
        for deldir in os.listdir(filedir):
            absdir = os.path.join(filedir, deldir)

            if not os.path.islink(absdir):
                mkdirtime = os.path.getmtime(absdir)
                timelist.append(mkdirtime)
        sortlist = sorted(timelist)
    
        for deldir in os.listdir(filedir):
            absdir = os.path.join(filedir, deldir)
            if not os.path.islink(absdir):
                if len(sortlist) > 2:
                    if os.path.getmtime(absdir) < sortlist[-2]:
                        shutil.rmtree(absdir)
                        print('%s delete ok!' % absdir)

    os.chdir(filedir)
    os.system('symlinks -d .')
    os.chdir(path)
