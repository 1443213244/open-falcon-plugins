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
    command = ''' ss -lntp|grep -v  "LISTEN     0"|wc -l  '''
    res = os.popen(command)
    res=res.readlines()
    for i in res:

        return {
        'listen-port':i.replace('\n', '')
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
            "timestamp": int(time.time()),
            "step": 60,
            "value": v,
            "counterType": "COUNTER",
            "tags": "listen=port"
            }

        playload_lst.append(playload)

    return playload_lst


def main():
    a=get_send_json()
    print(a)

main()
