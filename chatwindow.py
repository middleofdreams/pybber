# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,gobject,time,re

def savechat(guiclass,recipent,user,chat):
	if user==None or user=="None": user=recipent
	text="<b>-= <font color=blue>"+user+"</font></b>: "+chat
	text=text.replace(chr(13),"<br/>")
	text=text.replace("\n","<br/>")
	text=intolink(text)
	if recipent in guiclass.messages: 
		guiclass.messages[recipent]=guiclass.messages[recipent]+"<br/>"+text
	else : guiclass.messages[recipent]=text

def loadchat(guiclass,recipent):
	

	if recipent in guiclass.messages:
		html=guiclass.messages[recipent]
	else: html=""
	gobject.idle_add(guiclass.chat.load_html_string ,"<font size=-3>"+html, "file:///")
		
def copyfromchat(guiclass):
	guiclass.chat.copy_clipboard()


def intolink(urlstr):
	pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	pat2 = re.compile(r"(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	urlstr = pat1.sub(r'\1<a href="\2" target="_blank" title="\2">\3</a>', urlstr)
	urlstr = pat2.sub(r'\1<a href="http://\2" target="_blank" title="\2">\3</a>', urlstr)
	
	return urlstr
