# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,gobject,time

def savechat(guiclass,recipent,user,chat):
	if user==None or user=="None": user=recipent
	text="<b>-= <font color=blue>"+user+"</font></b>: "+chat
	text=text.replace(chr(13),"<br/>")
	text=text.replace("\n","<br/>")

	if recipent in guiclass.messages: 
		guiclass.messages[recipent]=guiclass.messages[recipent]+"<br/>"+text
	else : guiclass.messages[recipent]=text

def loadchat(guiclass,recipent):
	if recipent in guiclass.messages:
		html=guiclass.messages[recipent]
	else: html=""
	gobject.idle_add(guiclass.chat.load_html_string ,"<font size=-3>"+html, "file:///")
		
