
import json
import os
import requests
import http.cookiejar as cookielib
import time

class Jianshu:

    agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
    headers = {
        'Host': 'www.jianshu.com',
        'Referer': 'http://www.jianshu.com/',
        'User-Agent': agent,
        'Cookie': 'UM_distinctid=15acba07a534ff-058e8856965773-1d3b6853-1aeaa0-15acba07a54239; CNZZDATA1258679142=139791223-1489019205-%7C1493262381; _gat=1; remember_user_token=W1s1MTAwMV0sIiQyYSQxMCRtc3JidDFZei90T2tvWWNkdXRNajV1IiwiMTQ5NDU2OTgwNy44MDg2NTY3Il0%3D--d866b392fb0734f354d7172d50d0157513d95173; _session_id=ckxQYnRweXo1NGYrb1QyNzB5d1k1THFqM0ViLzNmQ2RsSDdBNC81Q0EwM3JPbnEweGduRnhITFNxYjRFVUQrRzREQzZKNnhhWlhWb2h1aUFlTmo2NlFRNWZLYUhiY3pMMUFPdnp2OG5kSEJ2TE9MdG95SCt4TmI3Uk9xRnoyRklBWmJ6VHIvSWFpYUV3amQyOG90WHMxT1ZOVnhVUkdqUUhTdzZBcmhnRnk3aG1tOExzQy9YMTV5bTRTbHFaSW1UVDdJTTJOWXVXNjNiTTJDZC9PaVVvRENpcXR4TlJ1a1RpK1l4NllEdUgvNlRIQkF5UmcvSHhXcnZQZktTMTY2SUFyVytoRHpQNkNUWHJoa0Uvb3FFSEJlZjhoZWhIRGdPdHE2UnQweXp6T0EvMVRKenlyV0tTSFZNbEw3RE1jN2lFeDRVMzJFb21PRDJrZGthaEg3VExGNUwzYnBSS2hIZlJxZ3VaN0ZmRTl6SHc1bDI2SndhbHlHQ0t4VGFBTFBzWks4a3NHWnZzVmhUNUlIK2VRSGVHTnVtaEFWSDRjbDg5LzdveEp5ZGs3Zz0tLUwrSE9mUzlZZDNrUUpwVDUxdGl2aVE9PQ%3D%3D--4acb1f693f5da4753c501f2a332499f72b8b9c5d; _ga=GA1.2.401893218.1489044269; _gid=GA1.2.1062414040.1494569811; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1493965041,1494212633,1494213218,1494554969; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1494569811'

    }

    upload_headers = {

        'Host': 'upload.qbox.me',
        'Referer': 'http://www.jianshu.com/writer',
        'origin': 'http://www.jianshu.com',
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

        imgs = self.getUploadImgs(art_dir)
        print(imgs)

        source_file_path = art_dir + os.path.sep + 'source.md'
        source_file = open(source_file_path, 'w', encoding='utf-8')
        content = self.makeArtContent(imgs)
        source_file.write(content)
        source_file.close()

    def makeArtContent(self, imgs):

        content = ['\n']
        for i in range(0, len(imgs)):
            content.append('![](' + imgs[i] + ')')

        return '\n\n\n'.join(content)

    def getUploadImgs(self, art_dir):

        img_dir = art_dir + os.path.sep + 'img/output'
        print(img_dir)
        imgs = []
        arr = os.listdir(img_dir)
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
        token = res['token']
        key = res['key']
        file_name_new = res['filename']
        img_url = res['url']


        img_url = self.postImgFile(img_file_path, token, key)
        print(img_url)
        return img_url


    def getImgFileToken(self, file_name):

        url = 'http://www.jianshu.com/upload_images/token.json'
        params = {

            'filename':file_name
        }
        login_page = self.session.get(url, headers = self.headers, params = params)
        # self.session.cookies.save()
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








