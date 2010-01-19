# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os

workpath=os.environ['HOME']+"/.pybber/archive"
prefs=workpath+"/prefs.db"

def is_created(recipent,day):
	path=workpath+"/"+recipent
	filepath=path+"/"+day+".html"
	
	if not os.path.isdir(workpath):
		os.makedirs(workpath)
	if not os.path.isdir(path):
		os.makedirs(path)
		f = open(filepath, "w")
		f.write("<html><title>Rozmowa z "+recipent+" z "+day+"</title><meta http-equiv='content-type' content='text/html; charset=UTF-8'></head><body>") 
		
def archive_append(chat,recipent,user,time,day):
	day=day.replace(" ","-")

	is_created(recipent,day)
	path=workpath+"/"+recipent
	filepath=path+"/"+day+".html"

	f = open(filepath, "a")
	f.write("<i>("+time+")</i><b> <font color=blue>"+user+"</font></b>: "+chat+"<br/>")	   
	
def load_last(gui,recipent,day):
	day=day.replace(" ","-")
	filepath=path+"/"+day+".html"
	#try:
	#	f = open(filepath, "r")
	#	text=f.read()
	#	text=text.split("<b/>")
	#	i=10
		
		#while 
def archive_loadlist(guiclass):
	index=guiclass.list.get_selection()
	index=index.get_selected()[1]
	recipent=guiclass.listmodel.get_value(index,4)
	path=workpath+"/"+recipent
	days=os.listdir(path)
	for day in days:
		day=day.rstrip('.html')
		print day
		guiclass.archivelist.get_model().append([day])
	
