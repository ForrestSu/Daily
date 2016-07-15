## Daily
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ForrestSu)  
This is a small tool to automatically submit RDM daily work, enjoy it!  
Attention: Please use it in **Company Network**!(Also you can connect **Company vpn**)  
## Author
[ForrestSu](https://github.com/ForrestSu)  
(Thanks [tqd](https://github.com/tanqidong) )

##Requirements
* Python 2.7+ 

## Installation
1. Install [Python 2.7](https://www.python.org/downloads/)+
2. `git clone  https://github.com/ForrestSu/Daily.git Daily`  
3. Modify Daily.txt file at Line 18,Like this:
```python  
  #type yourself Company Account Information  
  USERNAME = 'zhangsan12520'  
  PASSWORD = '12345678@A' 
``` 

##How To Use
1. Run `daily.py` first, will generate two files named `Daily.txt、Daily.log` in Current directory. (Daily.log record some log when this program is running.)
2. Write your Daily note into `daily.txt`. [here](#screenshots)
3. Run `daily.py` again, your Daily note will be post to PDM.

## AutoRun Once Everyday
**Windows**  
Use `Task Scheduler`
>Add `daily.vbs` into Windows scheduled tasks(**Pay Attention**:First modify the `daily.vbs` file path properly!)  

![RDM](https://github.com/ForrestSu/Daily/blob/master/png/taskschedule.png)

**Linux**  
Use `crontab`：run once from Monday to Friday  at 17:30  
>vi /etc/crontab 
>add `30 17 * * 1-5  python /etc/Daily/daily.py`

##Screenshots
![RDM](https://github.com/ForrestSu/Daily/blob/master/png/daily.png)

##FAQ
If you have some question, Welcome add issue.
