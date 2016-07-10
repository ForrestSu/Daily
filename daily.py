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
import RDM

#type yourself Company Account Information
USERNAME = 'zhangsan12520'
PASSWORD = '12345678@A'

##文件名
f_logfile = 'daily.log'
f_dailyfile = 'daily.txt'



'''
def readTaskDict():
    dict={}
    reader = open('Text.txt')
    text = reader.read()#全部内容读成字符串
    lines = text.split('\r\n')#处理一下就得到行数组了
    print(lines)
    return 'dict'
'''
def AutoSubmit():
    NOWDIR=sys.path[0]
    if not NOWDIR.endswith(os.sep):
        NOWDIR = NOWDIR + os.sep
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[%(levelname)s] %(message)s',
                datefmt='%a,%Y-%m-%d %H:%M:%S',
                filename=NOWDIR+f_logfile,
                filemode='a')
    myrdm = RDM.RDMBrowser()
    if not myrdm.Login(USERNAME,PASSWORD):
        logging.info('Login Fail !')
        exit(0) 
    logging.info('Login Successful.')
    dailyfile = NOWDIR+f_dailyfile
    #首次使用文件不存在，获取任务列表,然后退出
    if not os.path.exists(dailyfile):
        if myrdm.get_task_list(dailyfile):
            f.write(u'##请填写下面的内容,每条填写一行，行内按TAB分隔,日期按从小到大填写\r\n')
            f.write(u'日期\t任务序号\t时间\t工作内容\r\n')
            f.write(u'2016-07-04\t1\t5\t1.QDII学习\\n2.客户问题排查\r\n')
            f.write(u'2016-07-04\t1\t4\t1 QDII学习\r\n')
        logging.info(myrdm.getMsg())
        exit(0)

    '''下面只需要重文件中读取 未提交的行记录，逐步提交即可。'''
    
    '''
    readTaskDict();
    id_theme_develop = '965b35a7-afb4-4b96-9318-ec431ecf3376' #【日志】开发实现、单元测试等
    sdate='2016-07-06'
    note = OneNote(id_theme_develop,'1、策略交易批量委托服务修改',sdate,'10');
    #提交工作日志
    logging.info(RDM.submit(note))
    '''
    

if __name__ == '__main__':
    #每天自动提交青铜器
    AutoSubmit()
    
    
