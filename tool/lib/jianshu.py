
import json
import os
import requests
import http.cookiejar as cookielib
import time
import configparser
import re
from selenium import webdriver

conf_path = '/Users/zhuxu/Documents/mmjstool/synctoweb/syncart/sync.conf'
chromedriver_path = '/Users/zhuxu/Documents/mmjstool/chromedriver'

cf = configparser.RawConfigParser()
cf.read(conf_path)
username = cf.get('jianshu', 'username')
password = cf.get('jianshu', 'password')


class Jianshu:

    agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
    headers = {
        'Host': 'www.jianshu.com',
        'Referer': 'https://www.jianshu.com/',
        'User-Agent': agent,
        'Cookie': cf.get('jianshu', 'cookie')

    }

    upload_headers = {

        'Host': 'upload.qbox.me',
        'Referer': 'https://www.jianshu.com/writer',
        'origin': 'https://www.jianshu.com',
        'User-Agent': agent
    }

    session = requests.session()

    def __init__(self):

        print('jianshu init')
        self.session.cookies = cookielib.LWPCookieJar(filename='cookies_jianshu')
        
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print("Cookie 未能加载")


    def initAllArt(self, root_dir):

        arr = os.listdir(root_dir)
        for i in range(0, len(arr)):
            if not arr[i].startswith('.'):

                art_dir = root_dir + os.path.sep + arr[i]
                self.initArt(art_dir)

    def initArt(self, art_dir):

        try:
            imgs = self.getUploadImgs(art_dir)
            print(imgs)
        except:
            print("cookie error")
            cf.read(conf_path)
            self.headers['Cookie'] = self.getCookie(username, password)
            imgs = self.getUploadImgs(art_dir)


        source_file_path = art_dir + os.path.sep + 'source.md'
        source_file = open(source_file_path, 'w', encoding='utf-8')
        content = self.makeArtContent(imgs)
        source_file.write(content)
        source_file.close()

    def getCookie(self, username, password):

        url = 'https://www.jianshu.com/sign_in'
        driver = webdriver.Chrome(chromedriver_path)
        driver.get(url)
        time.sleep(10)
        print(username)
        driver.find_element_by_id('session_email_or_mobile_number').send_keys(username)
        driver.find_element_by_id('session_password').send_keys(password)

        input('去手动登录吧\n>  ')
        # 网页源码
        page = driver.page_source
        # print(page)

        pattern = r'(摹喵居士)'
        res = re.findall(pattern, page)
        print(res)

        cookies = driver.get_cookies()
        cookies_str = ''
        for item in cookies:
            cookies_str += item['name'] + '=' + item['value'] + ';'
        cf.set('jianshu', 'cookie', cookies_str)
        cf.write(open(conf_path, 'w'))

        # 关闭浏览器
        driver.close()

        return cookies_str


    def makeArtContent(self, imgs):

        content = ['\n']
        for i in range(0, len(imgs)):
            content.append('![](' + imgs[i] + '?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240' + ')')

        return '\n\n\n'.join(content)

    def getUploadImgs(self, art_dir):

        img_dir = art_dir + os.path.sep + 'img/output'
        print(img_dir)
        imgs = []
        arr = os.listdir(img_dir)
        arr.sort(key = str.lower)
        for i in range(0, len(arr)):
            # print(dir)
            if not arr[i].startswith('.'):
                print(arr[i])
                img_url = self.uploadImgFile(img_dir, arr[i])
                imgs.append(img_url)
        return imgs

    def uploadImgFile(self, img_dir, file_name):

        img_file_path = img_dir + os.path.sep + file_name

        res = self.getImgFileToken(file_name)
        print(res);
        token = res['token']
        key = res['key']
        # file_name_new = res['filename']
        # img_url = res['url']


        img_url = self.postImgFile(img_file_path, token, key)
        print(img_url)
        return img_url


    def getImgFileToken(self, file_name):

        url = 'https://www.jianshu.com/upload_images/token.json'
        params = {

            'filename':file_name
        }
        login_page = self.session.get(url, headers = self.headers, params = params)
        # self.session.cookies.save()
        print(login_page.text)
        # print(self.session.cookies)
        res = json.loads(login_page.text)
        return res

    def postImgFile(self, img_file_path, token, key):

        t = str(int(time.time() * 1000))

        # self.upload_headers['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundary' + t + ';'
        # print(self.upload_headers)

        files = {

            'file': open(img_file_path, 'rb')
        }

        post_data = {

            'token': token,
            'key': key

        }
        # print(files)

        post_url = 'https://upload.qbox.me/'

        login_page = self.session.post(post_url, data = post_data, files = files, headers = self.upload_headers);

        res = json.loads(login_page.text)
        return res['url']








