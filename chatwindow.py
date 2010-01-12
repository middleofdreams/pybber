# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,gobject,time
#-----------aktualizacja szerokosci wrappera i scrolldown
def update(guiclass,n):
	try:
		guiclass.renderer.props.wrap_width = int(guiclass.column.get_width())-int(10)
	except:
		pass
	n=guiclass.chat.get_path(n)
	guiclass.chatwindow.scroll_to_cell(n) 

def savechat(guiclass,recipent,user,chat):
	text="<b>-= <font color=blue>"+user+"</font></b>: "+chat
	
	if recipent in guiclass.messages: 
		guiclass.messages[recipent]=guiclass.messages[recipent]+"<br/>"+text
	else : guiclass.messages[recipent]=text

def loadchat(guiclass,recipent):
	if recipent in guiclass.messages:
		html=guiclass.messages[recipent]
	else: html=""
	gobject.idle_add(guiclass.chat.load_html_string ,"<font size=-3>"+html, "file:///")
		
	
	#guiclass.chat.scroll()
			#update(guiclass,n)
