#!/usr/local/bin/python3.5

import os
import sys
import subprocess

from lib.jianshu import Jianshu

if len(sys.argv) < 2:
    print('请输入目录')
    exit()

art_dir_path = sys.argv[1]
print(art_dir_path)

print(os.getcwd() + '/shell_pic.sh')

res = subprocess.check_output(['sudo', os.getcwd() + '/shell_pic.sh', art_dir_path])
print(res)

js = Jianshu()
# js.uploadImgFile('/Users/zhuxu/Documents/momiaojushi/write/art/463_20170515_看图说话52~幼儿园早饭/img/output', '2017-05-07 10-47-58___1810689.jpg')
js.initArt(art_dir_path)
# js.initAllArt('/Users/zhuxu/Documents/momiaojushi/write/art')
