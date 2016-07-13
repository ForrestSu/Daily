# -*- coding: UTF-8 -*-
#!/usr/bin/python
#'''  
# Author: sunquana@gmail.com
# github: ForrestSu
# Copyright @2016 licensed under the MIT license
# Date: 2016-06-20

## Attention: Please use it in company network! 
## Because Company network use https. Now,I do not support public network!

import time
import sys,os
import logging
import codecs
import re
import RDM
import random

#type yourself Company Account Information
USERNAME = 'zhangsan12520'
PASSWORD = '12345678@A'

##文件名
f_logfile = 'daily.log'
f_dailyfile = 'daily.txt'


def AutoSubmit():
    NOWDIR=sys.path[0]
    if not NOWDIR.endswith(os.sep):
        NOWDIR = NOWDIR + os.sep
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[%(levelname)s] %(message)s',
                datefmt='%a,%Y-%m-%d %H:%M:%S',
                filename=NOWDIR+f_logfile,
                filemode='a')
    try:
        myrdm = RDM.RDMBrowser()
        if not myrdm.Login(USERNAME,PASSWORD):
            logging.info('Login Fail !')
            exit(0) 
        logging.info('Login Successful.')
        dailyfile = NOWDIR+f_dailyfile
        #1 首次使用文件不存在，获取任务列表,然后退出
        if not os.path.exists(dailyfile):
            if myrdm.getTaskList(dailyfile):
                f = codecs.open(dailyfile,'a','utf-8') 
                f.write(u'##请填写下面的内容,注意：(1)每条填写一行,行内按TAB分隔;\r\n')
                f.write(u'##(2)每行记录前输入#号表示注释,提交成功后记录前默认加#号;\r\n')
                f.write(u'##(3)缺省记录Date将会被替换为当天日期。\r\n')
                f.write(u'日期\t任务序号\t时间\t工作内容\r\n')
                f.write(u'Date\t\t1\t8\t1.业务学习\r\n')
                f.write(u'2016-07-04\t1\t5\t1.业务学习\\n2.客户问题排查\r\n')
                f.write(u'2016-07-04\t1\t4\t1.业务学习\r\n')
                f.close()
            logging.info(myrdm.getMsg())
            exit(0)
        #2 读取txt并提交数据
        readTXT(myrdm,logging,dailyfile)
    except Exception as e:
        logging.error(e)

def readTXT(myrdm,log,dailyfile):
    #2 下面开启读取文件dailyfile并提交
    Nowdate=time.strftime('%Y-%m-%d',time.localtime(time.time())) 
    mydict={}
    flag=True
    writeback=''
    prefix=''
    linenumber=0
    f = open(dailyfile,'r')
    for line in f:
        sMessage=''
        linenumber+=1
        if line.startswith('#') or (len(line)<2): #过滤注释
            writeback=writeback+line
            continue
        if line.startswith('日期'):#接下来进入数据的提交逻辑
            flag=False
            writeback=writeback+line
            continue
        x = line.split()
        if flag and len(x)==3: # 放入字典中
            mydict[x[0]]=x[1]
        elif (len(x)==4):   # 限制为4
            if mydict.has_key(x[1]):
                prefix='#'
                if x[0].upper()=='DATE':
                    x[0]=Nowdate
                    prefix=''
                    sMessage='[缺省]'
                if x[0]<=Nowdate: # 直接忽略超前的daily note,暂不记录日志
                    line=prefix+line
                    #提交RDM
                    note=RDM.OneNote(mydict[x[1]],x[3],x[0],x[2]); 
                    logging.info(sMessage+myrdm.submit(note))
            else:
                logging.info('第['+str(linenumber)+']行的任务序号='+x[1]+',不存在!请检查！')
        else:
           logging.info('第['+str(linenumber)+']行记录,不书写符合规范！')
        writeback=writeback+line #这个需要写回txt文件

    f.close()
    f = codecs.open(dailyfile,'w','utf-8')
    f.write(unicode(writeback.replace('\n','\r\n'), "utf-8"))    
    f.close()  

if __name__ == '__main__':
    #每天自动提交青铜器
    AutoSubmit()
    
    
