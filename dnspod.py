# -*- coding:utf-8 -*-
'''
dnspod 自动提交更改的动态ip
安装方法:
1. pip install requests apscheduler argparse
2. python dnspod.py
'''

import requests
import re
import json
import os
import argparse
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
class dnspod(object):
    API_TOKEN = '登录的token'
    LANG = 'cn'
    FORMAT = 'json'
    MODIFY_URL = 'https://dnsapi.cn/Batch.Record.Modify'
    DOMAIN_LIST_URL = 'https://dnsapi.cn/Domain.List'
    RECORD_LIST_URL = 'https://dnsapi.cn/Record.List'
    RECORD_IDS = [ # 记录id
        1,
        2,
    ]
    LAST_IP_FILE_PATH = './ip'

    def __init__(self):
        if not os.path.isfile(self.LAST_IP_FILE_PATH):
            with open(self.LAST_IP_FILE_PATH, 'w') as f:
                f.write('')

    def run(self):
        with open(self.LAST_IP_FILE_PATH, 'r') as f:
            last_ip = f.read().strip()
        ip = self.get_local_ip()
        if last_ip != ip:
            with open(self.LAST_IP_FILE_PATH, 'w') as f:
                f.write(ip)
            self.update_domain(ip)
            print('[%s] %s ------ 已更新域名信息' % (now(), ip))
        else:
            print('[%s] %s ------ ip未发生变化' % (now(), ip))

    def get_domain_list(self):
        req_handle = requests.post(self.DOMAIN_LIST_URL, data={
            'login_token': self.API_TOKEN,
            'lang': self.LANG,
            'format': self.FORMAT,
        })
        print(json.dumps(json.loads(req_handle.text), indent=1))

    def get_record_list(self, domain_id):
        req_handle = requests.post(self.RECORD_LIST_URL, data={
            'login_token': self.API_TOKEN,
            'lang': self.LANG,
            'format': self.FORMAT,
            'domain_id': domain_id
        })
        print(json.dumps(json.loads(req_handle.text), indent=1))

    def update_domain(self, ip):
        record_id = ','.join(self.RECORD_IDS)
        try:
            req_handle = requests.post(self.MODIFY_URL, data={
                'login_token': self.API_TOKEN,
                'lang': self.LANG,
                'format': self.FORMAT,
                'record_id': record_id,
                'change': 'value',
                'change_to': ip
            })
            print(req_handle.text)
        except Exception as e:
            print(e)
            pass

    def get_local_ip(self):
        try:
            req_handle = requests.get('http://www.net.cn/static/customercare/yourip.asp')
        except:
            return False
        body = req_handle.text
        _match = re.compile(r'\d{1,}\.\d{1,}\.\d{1,}\.\d{1,}', re.I).findall(body)
        if _match:
            return _match[0]


now = lambda: str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help='获取你的域名列表', action='store_true')
    parser.add_argument("-r", help="获取指定域名的记录信息", type=int)
    parser.add_argument("-s", help="开始检测", action="store_true")
    args = parser.parse_args()
    if args.d:
        dnspod().get_domain_list()
    elif args.r:
        dnspod().get_record_list(args.r)
    elif args.s:
        print('Start...')
        sched = BlockingScheduler()
        sched.add_job(dnspod().run, 'interval', minutes=15)
        sched.start()
