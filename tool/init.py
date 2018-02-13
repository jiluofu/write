#!/usr/local/bin/python3

import os
import sys
import subprocess

from lib.jianshu import Jianshu


art_dir_path = os.getcwd()

print(art_dir_path)

shell_path = '/Users/zhuxu/Documents/mmjstool/write/tool/shell_pic.sh'

os.system(shell_path + ' .')


js = Jianshu()
js.initArt(art_dir_path)
