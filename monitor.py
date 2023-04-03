#!/bin/env python
# -*- coding: utf8 -*-
#author: operation department

import os
import sys
import time
import commands
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

logpath = os.path.dirname(sys.argv[0])
#######邮件配置#########
mailto_list=['*****@linekong.com']
mail_host="smtp.163.com"  #设置服务器
mail_user="********@163.com"   #用户名
mail_pass="******"   #口令
mail_name = "游戏服务进程监控报警"
nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
ip = commands.getstatusoutput('curl -s http://icanhazip.com/')
wip = ip[1].split(' ')[-1]

#####钉钉配置######
url = "钉钉群机器人地址"
title = "甄嬛传宕机报警"
content = "监控报警"
msg = """### 甄嬛传程序报警 \n
> content: %s \n
> 时间: %s \n
> 游戏区组：%s \n
> 状态: 重启 \n
"""



def monitorlog(string):
    #if yn == y : print('\033[1;32m%s\033[0m' % string) 
    filename = os.path.basename(sys.argv[0])
    f = open( '%s/%s.log' % (logpath,filename),'a')
    f.write('%s : %s : %s : %s\n' % (nowtime,filename,wip,string))
    f.close()
    
def dingtalk(quzu):
    headers = {"Content-Type": "application/json"}
    data = {"msgtype": "markdown",
        "markdown": {
            "title": title,
            "text":  msg %(content,nowtime,quzu)
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    print(r.text)
    
    
def send_mail(content):
    #messagelog = "%s Host  %s:%s connection failure \n" % (strtime, host[0], host[1])
    message = MIMEText (content, 'plain', 'utf-8')
    message['From'] = mail_user
    message['To'] = ','.join(mailto_list)
    subject = '程序宕机重启报警'
    message['Subject'] = Header (subject, 'utf-8')
       
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.starttls()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, mailto_list, message.as_string ())
        return True
    except Exception, e:
        print str(e)
        print 'error'
        return False
        pass

def  monitor():
   with open('/etc/passwd', 'r') as f:
      with open('output.txt', 'w') as out_file:
         for line in f:
            if line.startswith('server'):
               args = line.strip().split("::")[0]
               out_file.write(args + '\n')

   with open('output.txt', 'r') as out_file:
      for i in  out_file:
         username, _, _, uid  = i.strip().split(":")
         number = { 'username': username }
         number2 = { 'uid': uid }
         for x in number.values():
            for y in number2.values():
                commandformat = 'ps aux |  grep -v root | grep  -w %s | grep -w  "gameserver -c" | wc -l'
                process = commandformat % (y)
                outfile = commands.getstatusoutput(process)
                if outfile[1] == '1':
                    monitorlog('%s is running' % (x))
                else:
                    commandformatd = 'sudo -i -u %s /home/zhz/update/shutdown.sh gameserver '
                    commandformats = 'sudo -i -u %s /home/zhz/update/boot.sh gameserver'
                    processd = commandformatd % (x)
                    outfiled = commands.getstatusoutput(processd)
                    processs = commandformats % (x)
                    outfiles = commands.getstatusoutput(processs)
                    monitorlog('%s : %s : %s is restart complete, please checkout gameserverlog !!!' % (nowtime,wip,x))
                    send_mail('%s : %s : %s is restarting' % (nowtime,wip,x))
                    dingtalk(x)
 
if __name__ == "__main__":
    monitor()
