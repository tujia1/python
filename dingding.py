import json,requests,sys,time,datetime
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


job = sys.argv[1]
bianhao = sys.argv[2]
stat = sys.argv[3]

if str(stat) == 'success':
    name = '发布成功！'
    tupian = '![file](https://gd-prod-private.oss-cn-beijing.aliyuncs.com/yw/QQ%E6%88%AA%E5%9B%BE20201109153327.png)'
elif str(stat) == 'failure':
    name = '发布失败！'
    tupian = '![file](https://gd-prod-private.oss-cn-beijing.aliyuncs.com/yw/QQ%E6%88%AA%E5%9B%BE20201109163201.png)'
elif str(stat) == 'aborted':
    name = '发布取消！'
    tupian = '![file](https://gd-prod-private.oss-cn-beijing.aliyuncs.com/yw/QQ%E6%88%AA%E5%9B%BE20201109163201.png)'


url = "https://oapi.dingtalk.com/robot/send?access_token=****************"
title = job + " : " + stat
nowtime = datetime.datetime.now()
nowtime = str(nowtime.strftime('%Y-%m-%d %H:%M:%S'))
msg = """### %s \n
> 时间: %s \n
> 编号: #%s \n
> 地址: [工程链接](http://************/job/%s) \n
%s
"""

def Alert():
    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": msg %(title, nowtime, bianhao, job, tupian)
        }
    }

    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    print(r.text)

Alert()
