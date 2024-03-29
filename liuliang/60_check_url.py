#!/usr/bin/python
# coding: utf-8
import sys
import os
import time
import requests
import json
import re
from collections import defaultdict
import urllib3

urllib3.disable_warnings()

playload_lst = list()
ts = int(time.time())
urls = [
        "https://seller.xiapi.shopee.cn/webchat/conversations",
        "https://seller.vn.shopee.cn/webchat/conversations",
        "https://seller.ph.shopee.cn/webchat/conversations",
        "https://seller.sg.shopee.cn/webchat/conversations",
        "https://seller.id.shopee.cn/webchat/conversations",
        "https://seller.my.shopee.cn/webchat/conversations",
        "https://deo.shopeemobile.com/shopee/shopee-seller-live-ph/webchat/1.styles.41e680b4985003867eca.css",
        "https://deo.shopeesz.com/shopee/shopee-cnsc-live-sg/moduleshost/static/vendor/css/index.f2c4d3458500acf6fe57.css",
        "https://console.aws.amazon.com/support/home#/case/create",
        "https://sellercentral.amazon.com/",
        "https://fast.com",
        "https://shopify.com",
        "https://business.facebook.com",
        "https://api.ip.sb/ip"
        ]

def get_hostname():
    res_command = os.popen('hostname').read().strip()
    return res_command if res_command else 'unknown'

def check_url(urls):
    metric = defaultdict(dict)
    for url in urls:
        domain = url.split("/")
        try:
            response = requests.get(url,verify=False)
            if response.status_code == 200:
                metric[domain[2]]['url-status'] = 1

        except Exception as e:
            metric[domain[2]]['url-status'] = 0
    playload = get_send_json(metric)

def get_send_json(metric=None):
    for tag in metric.keys():
        for k, v in metric[tag].items():
            playload = {
                "endpoint": get_hostname(),
                "metric": k,
                "timestamp": int(time.time()),
                "step": 60,
                "value": v,
                "counterType": "GAUGE",
                "tags": "domain=%s" % tag
            }

            playload_lst.append(playload)

    return playload_lst



def main():
    check_url(urls)

main()
r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(playload_lst))
#print r.text
