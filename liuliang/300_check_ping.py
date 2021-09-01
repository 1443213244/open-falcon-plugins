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
ips=[
   '173.248.242.175',
   '69.172.75.87'
    ]
def get_mon_by_port():
    losss=[]
    avgs=[]
    for ip in ips:
        command='ping '+ip +' -c 5'
        print command
        res = os.popen(command)
        res=res.readlines()
        print res
        loss = re.compile(r'received, (.*?)% packet loss')
        avg=re.compile(r'mdev = .*/(.*?)/.*/.*')
        loss=loss.findall(res[-2])
        avg=avg.findall(res[-1])
        losss+=loss
        avgs+=avg
    return ips,losss,avgs


#收集主机名
def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'

playload_lst = list()

def get_send_json():
    metric = defaultdict(dict)
    print(metric)
    info_dict=get_mon_by_port()
    ip=info_dict[0]
    loss_name=['loss','avg']
    loss=info_dict[1]
    avg=info_dict[2]
    info_dict=dict(zip(ip,avg))
    info_dicts=dict(zip(ip,loss))
    
    for k,v in info_dict.items():
                playload = {
                "endpoint": get_hostname(),
                "metric": k,
                "timestamp": ts,
                "step": 300,
                "value": v,
                "counterType": "GAUGE",
                "tags": "listen=avg",
            }
                playload_lst.append(playload)
    for k,v in info_dicts.items():
                print k
                playload = {
                "endpoint": get_hostname(),
                "metric": k,
                "timestamp": ts,
                "step": 300,
                "value": v,
                "counterType": "GAUGE",
                "tags": "listen=loss",
            }
                playload_lst.append(playload)
    return playload_lst


def main():
    a=get_send_json()
    print(a)

main()
r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(playload_lst))
