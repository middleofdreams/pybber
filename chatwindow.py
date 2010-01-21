# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,gobject,time,re
from archive import *

def savechat(guiclass,recipent,user,chat,time,day):
	if user==None or user=="None": user=recipent
	text="<i>("+time+")</i><b> <font color=blue>"+user+"</font></b>: "+chat
	text=text.replace(chr(13),"<br/>")
	text=text.replace("\n","<br/>")
	text=intolink(text)
	if recipent in guiclass.messages: 
		guiclass.messages[recipent]=guiclass.messages[recipent]+"<br/>"+text
	else :
		
		 guiclass.messages[recipent]=text 
	archive_append(chat,recipent,user,time,day)

def loadchat(guiclass,recipent):
	if recipent in guiclass.messages:
		html=guiclass.messages[recipent]
	else: 
		html=load_last(recipent)
		guiclass.messages[recipent]=html
	guiclass.chat.load_html_string("", "file:///")
	html="<font size=-3>"+html+"</font size=-3>"
	gobject.idle_add(guiclass.chat.load_html_string,html, "file:///")
	#guiclass.chat.execute_script("document.innerHTML = '%s<br/>');" % html)


def updatechat(guiclass,recipent,user,chat,time):
	if user==None or user=="None": user=recipent
	text="<i>("+time+")</i><b> <font color=blue>"+user+"</font></b>: "+chat
	text=striptags(text)
	text=intolink(text)

	guiclass.chat.execute_script("appendtext('"+text+"');")

def copyfromchat(guiclass):
	guiclass.chat.copy_clipboard()
	

def intolink(urlstr):
	pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	pat2 = re.compile(r"(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	urlstr = pat1.sub(r'\1<a href="\2" target="_blank" title="\2">\3</a>', urlstr)
	urlstr = pat2.sub(r'\1<a href="http://\2" target="_blank" title="\2">\3</a>', urlstr)
	
	return urlstr
def messtime(ts):
	tp=time.mktime(time.strptime(ts,'%Y%m%dT%H:%M:%S'))+3600
	if time.localtime()[-1]: tp+=3600
	tp=time.localtime(tp)	
	tm=time.strftime("%H:%M:%S",tp)
	day=time.strftime("%d %m %Y",tp)
	return tm,day

def striptags(text):
	text=text.replace('"',"&#34;")
	text=text.replace("'","&#34;")
	text=text.replace("(","&#40;")
	text=text.replace(")","&#41;")
	text=text.replace(chr(13),"<br/>")
	text=text.replace("\n","<br/>")
	return text


def loadFinished(self,*a,**b):
	pos=self.chatwindow.get_vadjustment()	
	newpos=pos.get_upper()-pos.get_page_size()	
	pos.set_value(newpos)
	#pos.clamp_page(pos.get_upper(), pos.get_lower())
	self.chatwindow.set_vadjustment(pos) 
