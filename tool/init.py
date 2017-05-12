#!/usr/local/bin/python3.5

import os

from lib.jianshu import Jianshu

js = Jianshu()
# js.uploadImgFile('/Users/zhuxu/Documents/momiaojushi/write/art/463_20170515_看图说话52~幼儿园早饭/img/output', '2017-05-07 10-47-58___1810689.jpg')
# js.initArt('/Users/zhuxu/Documents/momiaojushi/write/art/463_20170515_看图说话52~幼儿园早饭')
js.initAllArt('/Users/zhuxu/Documents/momiaojushi/write/art')
