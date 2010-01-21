# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os,gobject,re,datetime

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
	f.write("<font size=-3><i>("+time+")</i><b> <font color=blue>"+user+"</font></b>: "+chat+"</font><br/>")	   
	
def load_last(recipent):
	now=datetime.datetime.now()
	day=now.strftime("%d-%m-%Y")
	path=workpath+"/"+recipent
	filepath=path+"/"+day+".html"
	try:
		f = open(filepath, "r")
		text=f.read()
		text=text.split("<br/>")
		html=""
		if len(text)>20:
			i=len(text)-10
			while not text[i].startswith("<font size=-3><i>("):
				i=i-1
			
			for y in range(i,len(text)):
				html=html+text[y]+"<br/>"
		else: 
			for i in text: html=html+i+"<br/>"
		html=html.rstrip("<br/>")+"<hr>"

	except:
		
		html=""
	f=open('script.js','r')
	script="<script type='text/javascript'>"+f.read()+"</script>"
	f.close()
	if not "<script" in html: 
		html=script+html
	return html
		
		#while 
def archive_loadlist(guiclass):
	index=guiclass.list.get_selection()
	index=index.get_selected()[1]
	recipent=guiclass.listmodel.get_value(index,4)
	path=workpath+"/"+recipent
	try:
		days=os.listdir(path)
	except:
		days=['Brak rozmów']
	days.sort(reverse=True)
	guiclass.archivelist.get_model().clear()
	for day in days:
		day=day.rstrip('.html')
		print day
		guiclass.archivelist.get_model().append([day,recipent])
	if days[0]==None or days[0]=="Brak rozmów": html="<center> Brak rozmów w archiwum"
	else: 
		path=workpath+"/"+recipent
		filepath=path+"/"+days[0]
		f = open(filepath, "r")
		html=f.read()
		f.close()
	guiclass.recipent=recipent
	guiclass.recipentname=guiclass.listmodel.get_value(index,0)	
	guiclass.window.set_title("Archiwum rozmowy z "+recipent)
	gobject.idle_add(guiclass.chat.load_html_string,html, "file:///")
	guiclass.wTree.get_widget("hbox2").hide()
	guiclass.archiveopen=recipent
	
def loadarchive(widget, row, col,guiclass):
	model = widget.get_model()
	text = model[row][0]
	text=text+".html"
	recipent=model[row][1]
	path=workpath+"/"+recipent
	filepath=path+"/"+text
	f = open(filepath, "r")
	html=f.read()
	f.close()
	html=html.replace(chr(13),"<br/>")
	html=html.replace("\n","<br/>")
	html=intolink(html)
	gobject.idle_add(guiclass.chat.load_html_string,html, "file:///")

		
def intolink(urlstr):
	pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	pat2 = re.compile(r"(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	urlstr = pat1.sub(r'\1<a href="\2" target="_blank" title="\2">\3</a>', urlstr)
	urlstr = pat2.sub(r'\1<a href="http://\2" target="_blank" title="\2">\3</a>', urlstr)
	return urlstr
