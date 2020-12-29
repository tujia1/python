#!/usr/bin/python
# -*- coding: utf-8 -*-


from ftplib import FTP
import time
import tarfile
import os


def ftpconnect(host, username, password):
    ftp = FTP()
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp


def downloadfile(ftp):
    bufsize = 1024
    remotepath=raw_input('Enter download path or flie :')
    fl=raw_input('Enter download flie :')
    ldpath='/tmp/tujia'
    os.chdir(ldpath) 
    fe=remotepath
    ftp.cwd(str(fe))
    fp = open(fl, 'wb')
    ftp.retrbinary('RETR ' + fl, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
    if os.path.isfile(fl):
        print 'Download successfully'
    else:
        print 'The download failed or the file did not exist !' 


if __name__ == "__main__":
   ftp = ftpconnect("120.92.17.138", "game_update", "WB4kFRL2") 
   downloadfile(ftp) 
        
