#!/bin/bash
pid=`ps -ef|grep server.py|grep python|awk '{print $2}'`
port=`ss -lnp |grep pid=$pid|grep tcp|sort -g|awk -F" " '{ print $5}'|awk -F":" '{ print $2}'|sort -g|head -1`
let end=port+252
sed -i 's/12269/'$port'/g'  /home/work/open-falcon/plugin/liuliang/60_liuliang.py
sed -i 's/12522/'$end'/g' /home/work/open-falcon/plugin/liuliang/60_liuliang.py
