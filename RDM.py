# -*- coding: UTF-8 -*-
#!/usr/bin/python
#'''  
# Author: sunquana@gmail.com
# github: ForrestSu
# Copyright @2016 licensed under the MIT license
# Date: 2016-06-20

## Attention: Please use it in company network! 
## Because public network use https. Now,I do not support public network!

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    import urllib2 as req_urllib
    from cookielib import CookieJar
except ImportError:
    import urllib.request as req_urllib
    from http.cookiejar import CookieJar

import re
import ssl
import codecs
import time
import random
import sys,os
import subprocess 

class OneNote:
    taskid = '' #任务号
    content = 'QDII学习'
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))  #日期,例如'2016-06-19'
    hour = '9'
    percent = str(random.randint(60,80))
    #定义构造方法  
    def __init__(self,sTaskid,sContent=content,sDate=date,sHour=hour,sPercent=percent): 
        self.taskid=sTaskid
        self.content=sContent
        self.date=sDate
        self.hour=sHour
        self.Percent=sPercent
    def toString(self):
        return "Date<%s>Work[%s]%sh" %(self.date,self.content,self.hour)
    
class RDMBrowser:
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
    #登录主页面
    url_login = 'https://hs-cas.hundsun.com/cas/login?service=http%3A%2F%2Fpm.hundsun.com%3A80%2Fj_acegi_cas_security_check'
    #post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据） 
    url_post = url_login
    #登陆成功后请求的页面
    url_homepage = 'http://pm.hundsun.com'
    url_main = url_homepage+'/main.do'
    url_task_list = url_homepage+'/pages/task/list/myTask.jsf'
    url_task_commit = url_homepage+'/pages/task/entity.jsf'
    url_getReportId_dwr = 'http://pm.hundsun.com/dwr/call/plaincall/jtaskEntityBean.dynGetReport.dwr'
    #定义构造方法  
    def __init__(self): 
        self.__sMessage = ''
        #初始化
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            opener = req_urllib.build_opener(
                req_urllib.HTTPCookieProcessor(CookieJar()))
            req_urllib.install_opener(opener)
        except:
            pass
    def getMsg(self):
        tempMsg = self.__sMessage
        self.__sMessage = ''
        return tempMsg

    def __getRequest(self,url, data=None):
        try:
            data = data.encode('utf-8')
        except:
            pass
        finally:
            return req_urllib.Request(url=url, data=data)
    def getInput(self,msg,default=0):
        #sqoci.getverify1(imgpath,'code.png')
        r=raw_input(msg)
        if r=='':
            return default
        return r
    def getverifyCode(self):
        #1 先下载图片
        request = self.__getRequest('https://hs-cas.hundsun.com/cas/kaptcha.jpg?'+str(random.randint(1,99)))
        response = req_urllib.urlopen(request)
        data = response.read()
        imgpath=sys.path[0]+os.sep+'png'+os.sep
        file=open(imgpath+'code.png', "wb")
        file.write(data)
        file.flush()
        file.close()
        if sys.platform.find('darwin') >= 0:
            subprocess.call(['open', imgpath+'code.png'])
        elif sys.platform.find('linux') >= 0:
            subprocess.call(['xdg-open', imgpath+'code.png'])
        else:
            os.startfile(imgpath+'code.png')
        retcode = self.getInput('input a verify:')
        return str(retcode)
    def __preLogin(self):
        #1 获取登陆主页面
        request = self.__getRequest(url=self.url_login)
        response = req_urllib.urlopen(request)
        data = response.read()

        #2 获取lt,execution
        # name="lt" value="LT-701812-OdXBeOW0AFNKlCfOBpaHKQBeWqCNWi-cas01.example.org"
        regx = r'name="lt" value="(\S+?)"'
        matches = re.search(regx, data)
        lt = matches.group(1)
        #print lt
        # name="execution" value="e7s1" 
        regx = r'name="execution" value="(\S+?)"'
        matches = re.search(regx, data)
        execution = matches.group(1)
        #print execution
        captcha =self.getverifyCode()
        return (lt,execution,captcha)

    def Login(self,username,password):
        lt,execution,captcha=self.__preLogin()
        #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
        headers = {'User-Agent' : self.user_agent,  
                   'Referer' : self.url_login}  
        #构造Post数据，他也是从抓大的包里分析得出的。  
        postData = {
                    'username':username,### 你的用户名
                    'password':password,    ### 你的密码，密码可能是明文传输也可能是密文，如果是密文需要调用相应的加密算法加密 
                    'captcha':captcha,        #验证码
                    'lt':lt,               ### 特有数据，不同网站可能不同
                    'execution':execution, ### 特有数据，不同网站可能不同 
                    '_eventId':'submit',   ### 事件类别
                    'submit': ''           
                    }  
        #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
        request = req_urllib.Request(self.url_post, urlencode(postData), headers)   
        response = req_urllib.urlopen(request)  
        text = response.read() 
        #print text 
        if '青铜器RDM' in  text:
            self.__sMessage='Login Successful! verifycode=['+captcha+']'
            return True
        self.__sMessage='Login Fail !verifycode=['+captcha+']'
        return False
    #获取任务列表
    def getTaskList(self,dailyfile):
        r = self.__getRequest(url=self.url_task_list)
        response = req_urllib.urlopen(r)
        data = response.read()
        regex = r'id="javax.faces.ViewState" value="(\S+?)"'
        matches = re.search(regex, data)
        javax_faces = matches.group(1)
        # print javax_faces
        #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
        headers = {'User-Agent' : self.user_agent,  
                   'Referer' : self.url_task_list} 
        postdata ={
            'AJAXREQUEST' : 'j_id_id3',
            'operate' : 'operate',
            'page' : '',
            'cate' : '0',
            'type' : 'TSK',
            'module' : 'TSK',
            'planId' : '',
            'refreshType' : '1', #首次为‘1’
            'isInit' : 'Y', #首次为Y
            'nodeId' : '',
            'projectIds' : '',
            'taskName' : '',
            'emptySearch' : '',
            'baseSearch' : '',
            'hasPlanOwner' : '',
            'showFCTask' : 'N',
            'condition' : '',
            'isOwner' : '',
            'light' : '',
            'pjtTask' : '',
            'userId' : '',
            'objectId' : '',
            'filterIds' : '',
            'operate:_path' : '',
            'operate:_fileName' : '',
            'operate:_fileContentType' : '',
            'javax.faces.ViewState' : javax_faces, 
            'operate:refreshFull':'operate:refreshFull'
        }
        r = req_urllib.Request(self.url_task_list,urlencode(postdata) , headers)  
        #print request  
        response = req_urllib.urlopen(r)  
        data = response.read().decode('utf8')
        
        regex_title = r'id=\'(\S+?)\' status'
        title_items = re.findall(regex_title, data)
        # dblclick();">【日志】设计、文档编写及评审</a>
        regex_taskid = ur'dblclick\(\);">([\w\W]+?)</a>'
        taskid_items = re.findall(regex_taskid, data)
        Counts=len(title_items)
        icount=0
        if(Counts == len(taskid_items)):
            f = codecs.open(dailyfile,'a','utf-8') 
            while(icount < Counts):
                content="%d\t%s\t%s\r\n"%(icount+1,title_items[icount],taskid_items[icount])
                f.write(content)
                icount=icount+1
            f.close()
            self.__sMessage = '成功获取'+str(Counts)+'个任务,已写入文件'+dailyfile
            return True
        else:
            self.__sMessage = '无法获取任务列表,ERROR=[任务数和task_id数目不等]'
            return False

    #这个值首次填报给空即可,后续修改需要先获取,否则无法修改
    #参考: http://www.aichengxu.com/view/47015
    def __get_report_id(self,taskid,sdate):
        ''' 
        callCount=1
        page=/pages/task/entity.jsf?taskId=965b35a7-afb4-4b96-9318-ec431ecf3376&action=1&planRight=&date=
        httpSessionId=
        scriptSessionId=750F49C3DA1731E1EF25170F88D6526D408
        c0-scriptName=jtaskEntityBean
        c0-methodName=dynGetReport
        c0-id=0
        c0-param0=string:965b35a7-afb4-4b96-9318-ec431ecf3376
        c0-param1=string:2016-06-08
        batchId=2
        ''' 
        url_params = '?taskId='+taskid+'&action=1&planRight=&date=' 
        headers = {'User-Agent' : self.user_agent,  
                   'Referer' : self.url_task_commit + url_params,
                   'Accept-Encoding':'gzip, deflate',
                   'Content-Type':'text/plain',
                   'Host':'pm.hundsun.com'} 
        #Accept-Encoding 、Content-Type 一定要设置，否则会请求失败
        postdata ='''callCount=1
page=/pages/task/entity.jsf%s
httpSessionId=
scriptSessionId=${scriptSessionId}
c0-scriptName=jtaskEntityBean
c0-methodName=dynGetReport
c0-id=0
c0-param0=string:%s
c0-param1=string:%s
batchId=1'''%(url_params,taskid,sdate)
        #print postdata
        r = req_urllib.Request(self.url_getReportId_dwr,postdata, headers)   
        response = req_urllib.urlopen(r)  
        data = response.read()
        #,["15ca2f18-99a9-4be6-99c4-dceddc57cf3d",
        regex = r',\["(\S*?)",'
        report_id = re.search(regex, data)
        return report_id.group(1)

    # 这个值只和任务(Taskid)相关,与日期无关
    def __get_javax_faces(self,taskid):
        # http://pm.hundsun.com/pages/task/entity.jsf?taskId=965b35a7-afb4-4b96-9318-ec431ecf3376&action=1&planRight=&date=
        url_tmp=self.url_task_commit+'?taskId='+taskid+'&action=1&planRight=&date='
        r = self.__getRequest(url=url_tmp)
        response = req_urllib.urlopen(r)
        data = response.read()
        regex = r'id="javax.faces.ViewState" value="(\S+?)"'
        matches = re.search(regex, data)
        return matches.group(1)
        #print javax_faces
        
    def submit(self,note):
        # 1 需要从dwr获取一个report_id
        report_id = self.__get_report_id(note.taskid,note.date)
        #print 'report_id=['+report_id+']'
        # 2 还需要GET获取新的javax.faces.ViewState
        javax_faces = self.__get_javax_faces(note.taskid) 
        # 3 组装数据，提交即可
        headers = {'User-Agent' : self.user_agent,  
                   'Referer' : self.url_task_commit+'?taskId='+note.taskid+'&action=1&planRight=&date='} 
        postdata ={
            'AJAXREQUEST' : 'j_id_id3',
            'taskForm' : 'taskForm',
            'report_action_date' : note.date,   #日期
            'report_rate' : note.percent,       #完成百分比
            'report_in_work' : note.hour,       #工作时长
            'report_end_date' : '',
            'report_remain_work' : '0',
            'operate_remark' : note.content,    #工作内容
            'report_question' : '',
            'objectId' : note.taskid,           #任务ID
            'taskId' : note.taskid,
            'workflowType' : 'TSK',
            'action' : '1',
            'ueditor_image_urls' : '',
            'report_id' : report_id, #每一天的唯一标识
            'javax.faces.ViewState' : javax_faces,
            'taskForm:save' : 'taskForm:save',
        }
        r = req_urllib.Request(self.url_task_commit,urlencode(postdata) , headers)   
        response = req_urllib.urlopen(r)  
        response.read()
        return 'report_id=['+report_id+'],'+note.toString()+',填报成功'
