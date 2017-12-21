#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from ftplib import FTP 
import ftplib as ftplib  
def ftp_up(filename,remotefilename): 
    ftp=FTP() 
    ftp.set_debuglevel(0)#打开调试级别2，显示详细信息;0为关闭调试信息 
    ftp.connect('192.168.0.214',21)#连接 
    ftp.login('yhf','123456')#登录，如果匿名登录则用空串代替即可 
    count=remotefilename.count('/')
    pathlist= remotefilename.split('/',count )
    dir=''
    cwdpath='/'
    print(len(pathlist))
    print(pathlist)
    pathlist.remove('')
    print(pathlist)
    writename=pathlist[len(pathlist)-1]
    print(writename)
    if len(pathlist)>1:
        for i in range(0,(len(pathlist)-1)):
            try:
                dir+=pathlist[i]+'/'
                print('ceshi'+dir)
                cwdpath+=pathlist[i]+'/'
                ftp.mkd(dir)
            except ftplib.all_errors:
                print('')
            else:
                print("内容写入文件成功")
    ftp.cwd(cwdpath)
    #print ftp.getwelcome()#显示ftp服务器欢迎信息 
    #ftp.cwd('xxx/xxx/') #选择操作目录 
    bufsize = 1024#设置缓冲块大小 
    file_handler = open(filename,'rb')#以读模式在本地打开文件 
    print(ftp)
    ftp.storbinary('STOR %s' % writename,file_handler,bufsize)#上传文件 
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit() 
    print("ftp up OK")
 
def ftp_down(filename,writename): 
    ftp=FTP() 
    ftp.set_debuglevel(0) 
    ftp.connect('192.168.0.214',21) 
    ftp.login('yhf','123456') 
    bufsize = 1024
    # filename = "20120904.rar" 
    file_handler = open(writename,'wb').write #以写模式在本地打开文件 
    ftp.retrbinary('RETR %s' % filename,file_handler,bufsize)#接收服务器上文件并写入本地文件 
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit() 
    print("ftp down OK")

# ftp_down('/test/79651.pdf','image/79651.pdf')

ii = "test/79651/79651.pdf"
print(ii.split('.')[0])