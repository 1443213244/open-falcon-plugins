#!/usr/bin/python
# coding: utf-8

import sys
import os
import time
import requests
import json
import re
from collections import defaultdict


ts = int(time.time())


def get_mon_by_port():
    #print port
    command = ''' ping 173.248.242.175 -c 5  '''
    res = os.popen(command)
    res=res.readlines()
    kk = re.compile(r'received, (.*?)% packet loss')
    res=kk.findall(res[-2])
    for i in res:

        return {
        'listen-db':i
    }


#收集主机名
def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'

playload_lst = list()

def get_send_json():
    metric = defaultdict(dict)
    print(metric)
    info_dict=get_mon_by_port()
    for k,v in info_dict.items():
        playload = {
            "endpoint": get_hostname(),
            "metric": k,
            "timestamp": ts,
            "step": 60,
            "value": v,
            "counterType": "GAUGE",
            "tags": "listen=db",
            }

        playload_lst.append(playload)

    return playload_lst


def main():
    a=get_send_json()
    print(a)

main()
r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(playload_lst))
