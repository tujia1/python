#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import socket
import select
import thread
import smtplib
from email.mime.text import MIMEText
from email.header import Header

 
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

def scan(ip_list, port):
    """
    scan() -> getaddresslist()

    getaddresslist() function returns the IP address of the list.
    """
    if not isinstance (ip_list, list):
        sys.exit ("Function getaddresslist() return error message: %s" % ip_list)
    strtime = time.strftime ('%Y-%m-%d_%H:%M:%S', time.localtime ())

    f = open ('/data/tujia/python/pythonscan.log', 'ab')
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
                mail_host = "smtp.163.com"  # 设置服务器
                mail_user = "*********@163.com"  # 用户名
                mail_pass = "******"  # 口令
                sender = '***********@163.com'
                receivers = ['*****@linekong.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
                messagelog = "%s Host  %s:%s connection failure \n" % (strtime, host[0], host[1])
                message = MIMEText (messagelog, 'plain', 'utf-8')
                message['From'] = "13718467661@163.com"
                message['To'] = "tujia@linekong.com"
                subject = '测试邮件'
                message['Subject'] = Header (subject, 'utf-8')
                smtpObj = smtplib.SMTP ()
                smtpObj.connect (mail_host, 25)  # 25 为 SMTP 端口号
                smtpObj.login (mail_user, mail_pass)
                smtpObj.sendmail (sender, receivers, message.as_string ())
               
    s.close()
    f.close()
                  



         
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
