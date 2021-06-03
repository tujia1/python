import socket
import os
import yaml
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask

app = Flask(__name__)

def Fileconfig():
    '''
    yaml文件导入分析
    '''
    ospath = os.path.dirname(os.path.realpath(__file__))
    yamlpath = os.path.join(ospath, "template.yaml")
    with open(yamlpath, "r", encoding="utf-8") as f:
        config = yaml.full_load(f)
        return config


def Exploreport(project, ip, port):
    '''
       用socket检查端口存活
    '''
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
    '''
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

@app.route("/metrics")
def ApiResponse():
    # 定义metrics仓库，存放多条数据
    checkport = Checkport()
    REGISTRY = CollectorRegistry(auto_describe=False)
    mesStatus = Gauge("sszj_port_monitor", "api response stats is:", ["project", "ip", "port"], registry=REGISTRY)
    for datas in checkport:
        project = "".join(datas.get("project"))
        ip = "".join(datas.get("host"))
        port = "".join(datas.get("port"))
        status = datas.get("status")
        mesStatus.labels(project, ip, port).set(status)
    return Response(prometheus_client.generate_latest(REGISTRY), mimetype="text/plain")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)
