# -*- coding: utf-8 -*-

import os
import re
import json
import datetime
import time
import requests


pat_info = re.compile('var def =(.*);!?')
pat_fin = re.compile("hasFlag: '(\d)',")

campus = None

def modify_json(res_json: dict) -> dict:
    # load default geo_api_info
    with open(os.path.join('resource', f'{campus}.json'), 'r') as ifile:
        res_json['geo_api_info'] = json.load(ifile)

    res_json['province'] = res_json['geo_api_info']['addressComponent']['province']
    res_json['city'] = res_json['geo_api_info']['addressComponent']['city']
    res_json['address'] = res_json['geo_api_info']['formattedAddress']
    res_json['area'] = ' '.join([
        res_json['province'],
        res_json['city'],
        res_json['geo_api_info']['addressComponent']['district']
    ])
    res_json['date'] = datetime.datetime.now().strftime("%Y%m%d")
    res_json['created'] = int(time.time())
    res_json['ismoved'] = 0
    return res_json


def checkin(cookies_dict: dict)->bool:
    # base data
    session = requests.session()
    url = 'https://wfw.scu.edu.cn/ncov/wap/default/index'
    cookiesJar = requests.utils.cookiejar_from_dict(
        cookies_dict, cookiejar=None, overwrite=True)
    session.cookies = cookiesJar
    resp = session.get(url=url)
    if resp.status_code != 200:
        print('[ERROR]', resp.status_code)
        return False

    html = resp.content.decode('utf-8')

    status = len(pat_fin.findall(html)) == 1
    if status: # had checkin
        print("[ERROR] already checkin today")
        session.close()
        return False

    res = pat_info.findall(html)
    if len(res) == 0:
        print('[ERROR] not found')
        return False
    res_json = json.loads(res[0])
    
    # load geo info & modify data
    modify_json(res_json)

    # post checkin data
    url = 'https://wfw.scu.edu.cn/ncov/wap/default/save'
    resp = session.post(url=url, data=res_json)
    if resp.status_code == 200:
        resp_json = json.loads(resp.content.decode('utf-8'))
        print(f'[INFO] 签到结果:{resp_json["m"]}')
        return True
    else:
        print(f'[ERROR] 签到失败:{resp.status_code} {resp.content.decode("utf-8")}')
        return False

def all_checkin(file:str):
    with open(file) as fd:
        data = json.loads(fd.read())
    for person in data:
        global campus
        campus=person["CAMPUS"]
        if checkin({
            'eai-sess': person["EAI_SESS"],
            'UUkey': person["UUKEY"]
        }):
            print(person["name"]+" has checkin")
        else:
            print(person["name"]+" failed to checkin")


if __name__ == '__main__':
    all_checkin("resource/people.json")
