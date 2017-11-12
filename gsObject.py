# -*- code:utf-8 -*-
# 
# 
# 
import threading,binascii
from Queue import Queue
from time import sleep
from console import console

class gsthreading(threading.Thread):
    def __init__(self,num, interval,lpfun):
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.interval = interval  
        self.thread_stop = False  
        self.lpfun=lpfun
    def run(self): 
        while not self.thread_stop: 
            self.lpfun()          
            sleep(0.5)  
            
    def stop(self):  
        self.thread_stop = True 

# 基本输入输出对象
# 工作模式：
# ---------------------------------------------------------
# 同步模式（sync）：独立的读写方法，由程序自主调用
# 双工模式（dupl）：后台自动读方法，在读之前会检查写缓存，如有则优先运行写方法，然后再读
#          该模式还可细化，是一次性将缓存内容写完，还是一个循环写一条
# 轮询模式（poll）：双工模式的细化，在读之前发送命令，比如寻卡
# 响应模式（resp）：
# 计划任务（plan）：
# 
# #
class object_sync:
    def __init__(self):
        self.isOpen=False
        self.__model="ascii"    # 传输模式
        self.task=None          # 数据处理函数
        self.__type="sync"      # 同步模式	    收发自己处理      sync
                                # 响应模式	    收到再发          resp
                                # 轮询模式	    发后收		       poll
                                # 双工模式      每次读前先发      dupl
                                # 计划任务      定时运行任务      plan
        self.dev=None
    def open(self):
        self.dev.open()
        self.isOpen=True
    def close(self):
        self.dev.close()
        self.isOpen=False
    def read(self,buff=None):
        data=""
        if not buff:
            while True:
                r=self.dev.read(1)
                if(r==''):break
                elif self.__model=='bin':data+=binascii.b2a_hex(r)   
                elif self.__model=='ascii':data+=chr(int(binascii.b2a_hex(r),16))
        else:data=self.dev.read()
        return data
    def write(self,data):
        #print "object_sync:",data
        if self.__model=='bin':self.dev.write(binascii.a2b_hex(data))
        elif self.__model=='ascii':self.dev.write(data) 
    def Model(self,value=None):
        if not value:return self.__model
        else:self.__model=value



class object_poll:
    def __init__(self,dev,cmd=None):
        self.dev=dev
        self.dev.__type="poll"
        self.receive_data=None
        self.__cmd=cmd

    def open(self):
        try:
            self.dev.open()
            self.thread=gsthreading(1,1,self.task)
            self.thread.start()
            self.dev.isOpen=True
            return True
        except:
            return False
    def close(self):
        self.thread=None
        self.dev.close()
        self.dev.isOpen=False
    def read(self,buff=None):
        if not buff:data=self.dev.read()
        else:data=self.dev.read(buff)
        return data
    def write(self,data):
        self.dev.write(data)
    def task(self):
        #print "task:",self.__cmd
        #print "object_poll",self.dev
        if self.__cmd!=None:self.dev.write(self.__cmd)
        data=self.read()
        if not self.receive_data:print data
        else:self.receive_data(data)
    def Model(self,value=None):
        if not value:return self.dev.Model()
        else:self.dev.Model(value)
    def Cmd(self,value=None):
        if not value:return self.__cmd
        else:self.__cmd=value

class object_dupl(object_poll):
    def __init__(self,dev):
        object_poll.__init__(self,dev,None)
        self.dev.__type="dupl"
        self.__write_buff=Queue(255)
    def write(self,data):
        self.__write_buff.put(data)
    def task(self):
        if not self.__write_buff.empty():
            self.dev.write(self.__write_buff.get())
        data=self.read()
        if not self.receive_data:print data
        else:self.receive_data(data)

class object_resp(object_poll):
    def __init__(self,dev):
        object_poll.__init__(self,dev,None)
        self.dev.__type="resp"

class object_plan(object_poll):
    def __init__(self,dev):
        object_poll.__init__(self,dev,None)
        self.dev.__type="plan"