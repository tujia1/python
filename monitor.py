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
mailto_list=['*****@linekong.com']
mail_host="smtp.163.com"  #设置服务器
mail_user="********@163.com"   #用户名
mail_pass="******"   #口令
mail_name = "游戏服务进程监控报警"
nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
ip = commands.getstatusoutput('curl -s http://icanhazip.com/')
wip = ip[1].split(' ')[-1]




def monitorlog(string):
    #if yn == y : print('\033[1;32m%s\033[0m' % string) 
    filename = os.path.basename(sys.argv[0])
    f = open( '%s/%s.log' % (logpath,filename),'a')
    f.write('%s : %s : %s : %s\n' % (nowtime,filename,wip,string))
    f.close()

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
    with open("/home/zhz/update/user.txt") as f:
        for line in f:
            args = line.split(":")
            number = dict(username = args[0])
            number2 = dict(uid = args[2])
            for x in number.values():
                for y in number2.values():
                    commandformat = 'ps aux |  grep -v root | grep  -w %s | grep -w  "gameserver -c" | wc -l'
                    process = commandformat % (y)
                    outfile = commands.getstatusoutput(process)
                    if outfile[1] == '1':
                        monitorlog('%s : %s : %s is running' % (nowtime,wip,x))
                    else:
                        commandformatd = 'sudo -i -u %s /home/zhz/update/shutdown.sh gameserver '
                        commandformats = 'sudo -i -u %s /home/zhz/update/boot.sh gameserver'
                        processd = commandformatd % (x)
                        outfiled = commands.getstatusoutput(processd)
                        processs = commandformats % (x) 
                        outfiles = commands.getstatusoutput(processs)
                        monitorlog('%s : %s : %s is restart complete, please checkout gameserverlog !!!' % (nowtime,wip,x))
                        send_mail('%s : %s : %s is restarting' % (nowtime,wip,x))
 
if __name__ == "__main__":
    monitor()
