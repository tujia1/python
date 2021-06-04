import socket
import os
import yaml
import prometheus_client
import requests
from prometheus_client import Gauge, Counter
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
app = Flask(__name__)

def Fileconfig():
    ospath = os.path.dirname(os.path.realpath(__file__))
    yamlpath = os.path.join(ospath, "template.yaml")
    with open(yamlpath, "r", encoding="utf-8") as f:
        config = yaml.full_load(f)
        return config

def Urlexport(url):
    ''' 利用requests模块返回http响应时间'''
    r = requests.get(url, timeout=1)
    time = r.elapsed.total_seconds()
    result_de = {"url": url, "time": time}
    return result_de


def Exploreport(project, ip, port):
    try:
        connet = socket.socket()
        connet.connect((ip, int(port)))
        socket.setdefaulttimeout(0.5)
        result_dic = {"project": project, "host": ip, "port": str(port), "status": 1}
        return result_dic
    except:
        result_dic = {"project": project, "host": ip, "port": str(port), "status": 0}
        return result_dic

def Checkport():
    data = Fileconfig()
    result_list = []
    for i in data.keys():
        iplist = data.get(i).get("host")
        ports = data.get(i).get("port")
        for ip in iplist:
            for port in ports:
                result_dic = Exploreport(i, ip, port)
                result_list.append(result_dic)
    return result_list

def CheckUrl():
    sul = Fileconfig()
    result_list1 = []
    for y in sul.keys():
        url1 = "".join(sul.get(y).get("url"))
        print(url1)
        result_dc = Urlexport(url1)
        result_list1.append(result_dc)
    return result_list1

@app.route("/metrics")
def ApiResponse():
    checkport = Checkport()
    checkurl = CheckUrl()
    REGISTRY = CollectorRegistry(auto_describe=False)
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
    CheckUrl()
    app.run(host="127.0.0.1", port="5000", debug=True)
