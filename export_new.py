#!/bin/env python
# -*- coding: utf8 -*-

import socket
import os
import yaml
import prometheus_client
import requests
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
app = Flask(__name__)
REGISTRY = CollectorRegistry(auto_describe=False)

# yaml文件解析
def Fileconfig():
    ospath = os.path.dirname(os.path.realpath(__file__))
    yamlpath = os.path.join(ospath, "template.yaml")
    with open(yamlpath, "r", encoding="utf-8") as f:
        config = yaml.full_load(f)
        return config

# 网址检测
def Urlexport(url):
    r = requests.get(url, timeout=1)
    time = r.elapsed.total_seconds()
    result_de = {"url": url, "time": time}
    return result_de

#  端口检测
def Exploreport(project, ip, port):
    try:
        connet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connet.connect((ip, int(port)))
        connet.settimeout(1)
        result_dic = {"project": project, "host": ip, "port": str(port), "status": 1}
        return result_dic
    except:
        result_dic = {"project": project, "host": ip, "port": str(port), "status": 0}
        return result_dic

# 端口检测数据
def Checkport():
    data = Fileconfig()
    result_list = []
    for i in data.keys():
        if i != "http":
            iplist = data.get(i).get("host")
            ports = data.get(i).get("port")
            for ip_port in iplist:
               try:
                   ip, port = ip_port.split(':')
                   result_dic = Exploreport(i, ip, port)
                   result_list.append(result_dic)
               except:
                       for port in ports:
                           result_dic = Exploreport(i, ip_port, port)
                           result_list.append(result_dic)
    return result_list

# 网站监测数据
def CheckUrl():
    sul = Fileconfig()
    result_list1 = []
    for y in sul.keys():
        if y == "http":
            url1 = "".join(sul.get(y).get("url"))
            result_dc = Urlexport(url1)
            result_list1.append(result_dc)
    return result_list1

# flask_api 展示数据prometheus_clinet转换为Gauge
@app.route("/metrics")
def ApiResponse():
    checkport = Checkport()
    checkurl = CheckUrl()
    mesStatus = Gauge("sszj_port_monitor", "api response stats is:", ["project", "ip", "port"], registry=REGISTRY)
    mesurl = Gauge("sszj_port_url", "api response http time:", ["url"], registry=REGISTRY)
    for datas in checkport:
        project = "".join(datas.get("project"))
        ip = "".join(datas.get("host"))
        port = "".join(datas.get("port"))
        status = datas.get("status")
        for data1 in checkurl:
            url = "".join(data1.get("url"))
            time = data1.get("time")
        mesStatus.labels(project, ip, port).set(status)
        mesurl.labels(url).set(time)
    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001", debug=True)
