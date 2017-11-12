#!/usr/bin/env python
# -*- coding: utf8 -*-
#####################################################
#   随身考勤机原型---数据库的简单操作
#            设计者   蒋宁
#####################################################
import binascii
import time
import RPi.GPIO as GPIO
import signal
import serial
from time import sleep
import os
import datetime
import Image
import ILI9341 as TFT
import Adafruit_GPIO.SPI as SPI
import ImageFont
import ImageDraw
import subprocess
import sqlite3
import MFRC522					#导入SPI  MFRC522读卡器模块
#显示屏SPI接口参数	
DC = 3		#18
RST = 25	#23
SPI_PORT = 0
SPI_DEVICE = 0
#显示屏初始设置
nu=1
x=0
y=0
r=10
g=250
b=200
jd=270
width=240
height=320
backcolor=[(0,0,0)]
backdata=backcolor*(width*height)
# 显示屏函数类Create TFT LCD display class.
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
# 初始化显示屏Initialize display.
disp.begin()
# 调入字体.
font = ImageFont.truetype('simhei.ttf', 24)
# 显示屏清屏函数
def clear(disp,backdata):
	disp.buffer.putdata(backdata)
# 显示屏清屏函数调用方法
#clear(disp,backdata)
# 创建可旋转显示文字的函数。
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
	text = text.decode('utf-8')	                                # 转换字符编码.
	draw = ImageDraw.Draw(image)	                            # 获取渲染字体的宽度和高度.
	width, height = draw.textsize(text, font=font)
	textimage = Image.new('RGBA', (width, height), (0,0,0,0))	# 创建一个透明背景的图像来存储文字.
	textdraw = ImageDraw.Draw(textimage)	                    # 渲染文字.
	textdraw.text((0,0), text, font=font, fill=fill)
	rotated = textimage.rotate(angle, expand=1)	                # 旋转文字图片.
	image.paste(rotated, position, rotated)	                    # 把文字粘贴到图像，作为透明遮罩.
# 获取IP地址函数
def myip():
	arg='ip route list' 
	p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE) 
	data = p.communicate() 
	split_data = data[0].split() 
	ipaddr = split_data[split_data.index('src')+1] 
	return ipaddr
# 蜂鸣器定义
def buzz(i):
	GPIO.setmode(GPIO.BCM) #BOARD)  
	GPIO.setup(27, GPIO.OUT)  #13
	j=1
	while j<(i+1):
		GPIO.output(27, GPIO.HIGH)  
		time.sleep(0.1)  
		GPIO.output(27, GPIO.LOW)  
		time.sleep(0.1)
		j=j+1
# 指示灯定义
def led(i,j):
	if i>2:
		l=18
	elif i==1:
		l=18
	elif i==2:
		l=17
	GPIO.setmode(GPIO.BCM)  
	GPIO.setup(l, GPIO.OUT)  
	if j==1:
		GPIO.output(l, GPIO.HIGH)  
	else:  
		GPIO.output(l, GPIO.LOW) 

#######################################
#    数据库操作处理环节
#--------------------------------------
# sskq.db is a file in the working directory.
conn = sqlite3.connect("sskq.db")	# 连接一个数据库
conn.text_factory=str				# 定义表中文本属性
c = conn.cursor()					# 定义一个光标
# 删除一个数据表
#	conn.execute('DROP TABLE xuesen')
# 创建一个数据表create tables
conn.execute("CREATE TABLE IF NOT EXISTS xuesen(xuehao text, uid text, name text)")
# 保存改变save the changes
conn.commit()
# 关闭数据库连接close the connection with the database
conn.close()
conn = sqlite3.connect("sskq.db")
conn.text_factory=str
c    = conn.cursor()
# 查询指定字段内容
#c.execute("select * from xuesen")# where uid like '7a7d5ed0'
#print c.fetchone()
x=0
while x<1:
# 修改指定记录某字段内容，并且显示出来
	xh=u'2017090005'
	xm=u'徐立利'
	id=u'c1d27f36'
	c.execute("update xuesen set xuehao ='"+xh+"'  where uid='"+id+"'")		# 指定uid修改学号
	c.execute("update xuesen set name ='"+xm+"'  where uid='"+id+"'")		# 指定uid修改姓名
	conn.commit() 
	c.execute("select * from xuesen where uid like '"+id+"'")
	js=c.fetchall()
	print js					# 这种方法显示内容是汉字的字段会出现16进制数值
#	print js[0],js[1],js[2]		# 这种方法正常显示内容是汉字的字段

# 删除全部记录
#	conn.execute("delete from xuesen")  
#	conn.commit() 
# 检查原有记录数	
#	c.execute('select * from xuesen')	# 检索数据表
#	sjk=(c.fetchall())					# 把数据表全部记录读入一个数组列表
#	print sjk
#	total=len(sjk)						# 获取数据表记录的数目（列表的行数）
#	print "原有记录数:",total
# 列出现有全部记录
	c.execute('select * from xuesen')
	sjk=(c.fetchall())
#	print sjk
	n=len(sjk)
	print "现有记录数:",n
	i=0
	c.execute('select * from xuesen')
	while i<n:
		print i,")",(c.fetchone())
		i+=1
	x+=1
conn.close()


