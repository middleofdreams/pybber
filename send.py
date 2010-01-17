# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,time,gobject
from chatwindow import *

def sendmsg(guiclass):
	
	buffer=guiclass.message.get_buffer()
	start_iter=buffer.get_start_iter()
	end_iter=buffer.get_end_iter()
	msg=buffer.get_text(start_iter, end_iter, include_hidden_chars=True)
	#buffer.select_range(end_iter,start_iter)
	buffer.set_text("")
	#buffer.backspace(end_iter, False, True)
	#buffer.backspace(start_iter, False, True)
	start_iter=buffer.get_start_iter()
	end_iter=buffer.get_end_iter()
	buffer.delete(start_iter,end_iter)
	#buffer.backspace(end_iter, False, True)
	#buffer.backspace(start_iter, False, True)
	buffer.place_cursor(buffer.get_iter_at_line_offset(0,0))
	start, end = buffer.get_bounds()
	buffer.select_range(start,start)
	#buffer.backspace(buffer.get_end_iter(), True, True)
	#buffer.delete_interactive(buffer.get_start_iter(),buffer.get_end_iter(),True)
	

	# msg=str("ME:"+msg)
	if msg!="":
		ts=guiclass.connection.send(msg)
		guiclass.staticon.set_blinking(False)
		time,day=messtime(ts)
		savechat(guiclass,guiclass.recipent,"<font color=red>"+guiclass.settings.me+"</font>",msg,time,day)
		gobject.idle_add(loadchat,guiclass,guiclass.recipent)
		#n=guiclass.chat.append(["-= Me : "+msg])
		#update(guiclass,n)
