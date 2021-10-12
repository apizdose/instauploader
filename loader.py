import json
import subprocess
import random
import time
import csv
import re
import requests
from datetime import datetime, timedelta
import os
from PIL import Image
import glob
import shutil
from os import path

print('''Hello. I am a instagram bot, who uploading random photo across your accounts list round robin.
Now if I don't find, im create two folders. Plz put the photos in "album" folder.
In folder "trash" will be processed photos after posting.
And if you fill the form with logins press "Enter" on login and password question.
Also you must set time range to define frequency of your posting. From and to in seconds (in default it is 20000 to 30000 equivalent ~5,5 to 8 hours).

Note! Frequency is per post, NOT per account.
Note! Fill up the directory "album" before starting.
''')

if not os.path.isdir('album'):
    os.mkdir('album')
    print('Directory album created, put you images here!')
if not os.path.isdir('trash'):
    os.mkdir('trash')    

loginform=input('Login:  ') or ""
passwordform=input('Password:  ') or ""
#########################################
####Here your logins and passwords.#####
########################################
if os.path.isfile('login.txt'):
    logins={}
    with open('login.txt','r') as file:
        lgns = file.read().splitlines()
        for i in lgns:
            slic=i.split(":")
            logins[slic[0]]=slic[1]
            
    loginbase = [(k, v) for k, v in logins.items()]
    print(logins)

frfrom=input('Frequency from (seconds):  ') or "20000"
frto=input('Frequency to (seconds):  ') or "30000"
frfrom=int(frfrom)
frto=int(frto)

spam = False
XInstagramAJAX = csrftoken = ds_user_id = sessionid = ig_did = mid = ig_nrcb = False
XIGAppID = input('Paste XIGAppID or press enter to default: ') or "1217981644879628"
print('IGAppid for your version is: '+XIGAppID)


printtags='''
'''

def taggen():
    with open('tags.txt','r') as file:
        tags = file.read().splitlines()

        random.shuffle(tags)
        cnttag=random.randint(10,25)
        text = ' '.join(tags[:cnttag])

        capt=f'''.
.
.
{text}'''
        return capt

def smilegen():
    with open('smiles.txt','r', encoding='utf-8') as file:
        smiles = file.read().splitlines()

        random.shuffle(smiles)

        smiletext = ''.join(smiles)
        return smiletext
    
#Open session
def sessionData():

    #link = 'https://www.instagram.com/accounts/login/'
    link = 'https://www.instagram.com/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    localtime = int(datetime.now().timestamp())

#Login and password.
    payload = {
        'username': loginform,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{localtime}:{passwordform}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }
#Cookie and headers req.
    with requests.Session() as s:
        r = s.get(link, headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/"})
        csrf = re.findall(r"csrf_token\":\"(.*?)\"",r.text)[0]
        globals()['XInstagramAJAX'] = re.findall(r"rollout_hash\":\"(.*?)\"",r.text)[0]
        coo = dict(r.cookies)
        print('Cookies created.')
        
        


        r = s.post(login_url,data=payload,headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken":csrf
        })
        
        
        if r.status_code==403 or r.status_code==429:
            global spam 
            spam = True
            print("ERROR "+str(r.status_code)+" >>> "+r.text)
            timesleep =  datetime.now() + timedelta(seconds=10000)
            print("SLEEPING from "+str(datetime.now())+" to "+str(timesleep))
            time.sleep(10000)
            sessionData()
            

        else:
            cookies=dict(r.cookies)
            res = [(k, v) for k, v in cookies.items()]
            for i in res:globals()[i[0]] = i[1]
            print(r.status_code)
            print('\n\nConnected.')

def photoload(imagefile):
    with requests.Session() as s:
        filelengh = os.path.getsize(imagefile)
        lengh=str(filelengh)

        im = Image.open(imagefile)
        (imwidth, imheight) = im.size


        mtime = int(datetime.now().timestamp())
        microtime = str(mtime)
        #print(microtime)
        #print('width is: ' + str(imwidth) + '......height is: ' + str(imheight))
        headers={
                            'Host': 'i.instagram.com',
                            'Connection': 'keep-alive',
                            'Content-Length': lengh,
                            'X-Entity-Type': 'image/jpeg',
                            'X-IG-App-ID': XIGAppID,
                            'X-Entity-Name': f'fb_uploader_{microtime}',
                            'Offset': '0',
                            'sec-ch-ua-mobile': '?1',
                            'X-Instagram-AJAX': XInstagramAJAX,
                            'Content-Type': 'image/jpeg',
                            'Accept': '*/*',
                            'X-Instagram-Rupload-Params': f'{{"media_type":1,"upload_id":{microtime},"upload_media_height":{imheight},"upload_media_width":{imwidth}}}',
                            'X-ASBD-ID': '198387',
                            'X-Entity-Length': lengh,
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
                            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                            'sec-ch-ua-platform': '"Android"',
                            'Origin': 'https://www.instagram.com',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.instagram.com/',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
                            "Cookie": f'mid={mid}; ig_did={ig_did}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}',
                        }

        r = s.post(f'https://www.instagram.com/rupload_igphoto/fb_uploader_{microtime}', data=open(imagefile, "rb"), headers=headers)
        print('\n\n'+str(r.status_code))
        print(r.text)
        print('\nWaiting a few seconds...')
        time.sleep(random.randint(5,25))

        sheaders={
        'Host': 'i.instagram.com',
        'Connection': 'keep-alive',
        'Content-Length': '525',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'X-IG-App-ID': XIGAppID,
        'X-IG-WWW-Claim': 'hmac.AR1DI1g2Zh_2iUcb41tVL8yS6rqCJFOBYVA0p7idEuUHM7NA',
        'sec-ch-ua-mobile': '?1',
        'X-Instagram-AJAX': XInstagramAJAX,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
        'X-ASBD-ID': '198387',
        'X-CSRFToken': csrftoken,
        'sec-ch-ua-platform': '"Android"',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Cookie': f'mid={mid}; ig_did={ig_did}; fbm_124024574287414=base_domain=.instagram.com; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}',
            }


        printtags=taggen()
        comm = smilegen()
        
        sbody = {


        'source_type': 'library',
        'caption': f'{comm}\n{printtags}',
        'upcoming_event':'' ,
        'upload_id': microtime,
        'geotag_enabled': 'true',
        'location': '{"lat":48.527823421176,"lng":8.0762835113124,"facebook_places_id":108109851420734}',
        'usertags':'' ,
        'custom_accessibility_caption':'', 
        'disable_comments': '0',

            
            }

        r = s.post('https://www.instagram.com/create/configure/', data=sbody, headers=sheaders)

        print('\n\n'+str(r.status_code))
        #print(sbody)

def logout():
    headers={
        'Host': 'i.instagram.com',
        'Connection': 'keep-alive',
        'Content-Length': '525',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'X-IG-App-ID': XIGAppID,
        'X-IG-WWW-Claim': 'hmac.AR1DI1g2Zh_2iUcb41tVL8yS6rqCJFOBYVA0p7idEuUHM7NA',
        'sec-ch-ua-mobile': '?1',
        'X-Instagram-AJAX': XInstagramAJAX,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36',
        'X-ASBD-ID': '198387',
        'X-CSRFToken': csrftoken,
        'sec-ch-ua-platform': '"Android"',
        'Origin': 'https://www.instagram.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        'Cookie': f'mid={mid}; ig_did={ig_did}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessionid}',
            }

    body = {
        'one_tap_app_login': '0',
        'user_id': ds_user_id,          
            }

    with requests.Session() as s:
        r = s.post('https://www.instagram.com/accounts/logout/ajax/', data=body, headers=headers)
        print(r.status_code)
        #print(r.text)
        print('\n\nLogouted')
        
        
def runpost():
    countdata=0
    while True:
        if os.path.isfile('login.txt'):
            global loginform
            loginform=loginbase[countdata][0]
            global passwordform
            passwordform=loginbase[countdata][1]
            countdata+=1
        
            if countdata==len(loginbase):
                countdata=0
            
        time.sleep(1)
        mkfiles = glob.glob("album/*.jpg")#Collecting photos.
        try:
            numb=random.randint(0,(len(mkfiles)-1))
            #print(numb)
        
        except: print(bool(mkfiles))
        if bool(mkfiles):
            file = mkfiles[int(numb)]
            sessionData()
            print('Logined '+loginform+' Waiting to logoff 5-10min to post.')
            time.sleep(random.randint(300,600))
            photoload(file)
            print('Post from '+loginform+' with '+file+' created.\n\nWaiting to logoff 5-10min.')
            time.sleep(random.randint(300,600))
            logout()
            destination_path = "Trash"
            new_location = shutil.move(file, destination_path)
            #print(bool(mkfiles))
            global frfrom
            global frto
            sltime=random.randint(frfrom,frto)
            tsleep =  datetime.now() + timedelta(seconds=sltime)
            print("SLEEPING from "+str(datetime.now())+" to "+str(tsleep))
            time.sleep(sltime)
        else:
            print ("Album is full!")
            break

if __name__ == "__main__":
    runpost()
