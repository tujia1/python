#!/usr/local/python27/bin/python
# -*- coding: utf8 -*-
db={}
# 如果是新用户，这需要注册

def newuser ():
    prompt='请输入注册账号：'
    while True:
        name=raw_input(prompt)
        if db.has_key(name):
           prompt='您注册的账号已存在，请重新注册。'
           continue
        else:
            password=raw_input('请输入密码：')
            db[name]=password
            break


#如果已经注册，这需要登录
def olduser ():
    name=raw_input('请输入登录账号：')
    password=raw_input('请输入账号密码：')
    userpwd=db.get(name)
    if userpwd == password:
       print 'Welcome to login',name
    else:
       print 'Login account or password error, Please log in again.'

#显示系统界面
def showmeu ():
    prompt='请输入用户状态(n: 注册  e: 登录)：'
    con = False
    while not con:
        chosen = False
        while not chosen:
            try:
                choice=raw_input(prompt).strip()[0].lower()
            except(EOFError,KeyboardInterrupt):
                choice='q'
            print '您按下了【%s】键' % choice
            if choice  not in 'neq':
                print'您输入的内容不合法，请重新输入：'
            else:
                chosen = True
                con = True
            if  choice == 'n': 
                newuser()
            elif choice == 'e':
                olduser()
            else:
                 showmeu()

                
showmeu()













            
                 
