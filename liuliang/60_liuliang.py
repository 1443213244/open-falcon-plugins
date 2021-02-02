#!/usr/bin/python
# coding: utf-8

import sys
import os
import time
import requests
import json
import re

ts = int(time.time())
payload_lst = []


def add_iptables_port(port):
    os.system('iptables -I INPUT -p tcp --dport '+str(port))


def get_mon_by_port(port):
    #print port
    command = ''' iptables -L -n -v -x| grep {}'''.format(port)
    res = os.popen(command)
    res=res.readlines()

    if res:
        res = ','.join(filter(lambda x: x, res[0].split(' '))).split(',')
        #res=res[0].replace(" ","")
        pkt=res[0]
        byte=res[1]
        return {
            'packet-received': pkt,
            'byte-received': byte
        }
    else:
        add_iptables_port(port)


def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'


def get_send_json(port):
    info_dict = get_mon_by_port(port)
    try:
        for k, v in info_dict.items():
            payload = {
                    "endpoint": get_hostname(),
                    "metric": k,
                    "timestamp": ts,
                    "step": 60,
                    "value": v,
                    "counterType": "COUNTER",
                    "tags": "port={port}".format(port=port)
                }
            payload_lst.append(payload)
    except Exception as e:
        print e


def main():
    a=[]
    for i in range(12269,12522):
        a.append(i)
    monitor_port=set(a)

    for j in monitor_port:
        get_send_json(j)

main()
print payload_lst
r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload_lst))
#print r.text

