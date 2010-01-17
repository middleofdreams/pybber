# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,time,gobject
from chatwindow import *

def sendmsg(guiclass):
	
	buffer=guiclass.message.get_buffer()
	start_iter=buffer.get_start_iter()
	end_iter=buffer.get_end_iter()
	msg=buffer.get_text(start_iter, end_iter, include_hidden_chars=True)
	buffer.set_text("")
	msg=msg.replace("<","&lt;")
	msg=msg.replace("<","&gt;")

	# msg=str("ME:"+msg)
	if msg!="":
		ts=guiclass.connection.send(msg)
		guiclass.staticon.set_blinking(False)
		time,day=messtime(ts)
		savechat(guiclass,guiclass.recipent,"<font color=red>"+guiclass.settings.me+"</font>",msg,time,day)
		gobject.idle_add(loadchat,guiclass,guiclass.recipent)
		#n=guiclass.chat.append(["-= Me : "+msg])
		#update(guiclass,n)
