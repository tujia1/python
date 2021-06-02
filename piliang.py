#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import socket
import select
import thread
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header


mailto_list=['*****@linekong.com']
mail_host="smtp.163.com"  #设置服务器
mail_user="********@163.com"   #用户名
mail_pass="******"   #口令
mail_name = "游戏服务端口报警"

 
def getaddresslist(addr):
    """
    getaddresslist(addr) -> IP address file

    IP address read from the file.
    """
    try:
        with open(addr, "r") as ip_list:
            lines = ip_list.readlines()
            address = [line.strip().split(" ")[0] for line in lines]
        return address
    except (IOError, IndexError), e:
        return str(e)

def getaddressport(addr):
    try:
        with open(addr, "r") as port:
        #with open('/data/tujia/python/1', "r") as port:
            lines = port.readlines()
            scanport = [line.strip().split(" ")[1] for line in lines]
        return scanport
    except (IOError, IndexError), e:
        return str(e)
     
def send_mail(context):
    message = MIMEText (content, 'plain', 'utf-8')
    message['From'] = mail_user
    message['To'] = ','.join(mailto_list)
    subject = '端口报警'
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

def scan(ip_list, port):
    """
    scan() -> getaddresslist()

    getaddresslist() function returns the IP address of the list.
    """
    if not isinstance (ip_list, list):
        sys.exit ("Function getaddresslist() return error message: %s" % ip_list)
    strtime = time.strftime ('%Y-%m-%d_%H:%M:%S', time.localtime ())

    open ('/data/tujia/python/pythonscan.log', 'ab') as f:
    for addr in ip_list:
        for scanport in port:
            host = (addr,int(scanport))
            try:
                s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout (5)
                s.connect (host)
                print ("%s Host  %s:%s connection success. \n" % (strtime, host[0], host[1]))
                # f.write("%s Host  %s:%s connection success. \n" % ( strtime,  host[0], host[1]))
            except Exception, e:
                f.write ("%s Host %s:%s connection failure: %s. \n" % (strtime, host[0], host[1], e))
                send_mail("%s Host  %s:%s connection failure \n" % (strtime, host[0], host[1]))
               
                  



         
if __name__ == '__main__':

    addrs = sys.argv[1]
    #isNone = True
    #while isNone:
        #scanport = sys.argv[2]
        #scanport = raw_input("Enter the scan port: ")
        #if scanport:
            #isNone = False
        #else:
            #continue
    scan(getaddresslist(addrs),getaddressport(addrs))
