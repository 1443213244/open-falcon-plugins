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


def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'


def get_send_json(port):
    info_dict = get_mon_by_port(port)
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


def main():
    monitor_port = {
        10157,
        12308
    }

    for port in monitor_port:
        get_send_json(port)

main()
print payload_lst
r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload_lst))
#print r.text
