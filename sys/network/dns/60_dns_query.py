#!/usr/bin/python
#-*- coding:utf-8 -*-

import os, sys, re
import json

from dns.resolver import Resolver
import dns.resolver
import requests
import time
import urllib2, base64
from socket import *

PATH = os.path.dirname(os.path.realpath(__file__))
file = PATH+'/domain'
timestamp = int(time.time())
step = 60
counterType = "GAUGE"
data = []

def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'

def checkDNS(domain):
    try:
        res = dns.resolver.Resolver()
        res.lifetime = 1
        res.timeout = 1
        query = res.query(domain, 'A')
        if query.response.answer:
           result = 1
    except:
        result = 0
    return result


def updateData(tags = '', value = ''):
    endpoint = get_hostname()
    metric = "network"
    key = "dns"
    timestamp = int(time.time())
    step = 60
    vtype = "GAUGE"

    i = {
            'Metric' :'%s.%s'%(metric,key),
            'Endpoint': endpoint,
            'Timestamp': timestamp,
            'Step': step,
            'value': value,
            'CounterType': vtype,
            'TAGS': tags
            }
    return i

p = []

with open(file) as f:
    for line in f:
        results = re.findall("(\S+)",line)
        domain = results[0]
        description = results[1]
        # tags = "project=ops,"
        tags = "description=%s"%(description)
        value = checkDNS(domain)

        p.append(updateData(tags,value))

r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(p, sort_keys=True,indent = 4))
print r.text
