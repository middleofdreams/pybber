# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,time,gobject
from chatwindow import *

def sendmsg(guiclass):
	
  msg=guiclass.message.get_text()
  guiclass.message.set_text("")
 # msg=str("ME:"+msg)
  if msg!="":
	  ts=guiclass.connection.send(msg)
	  guiclass.staticon.set_blinking(False)
	  time,day=messtime(ts)
	  savechat(guiclass,guiclass.recipent,"<font color=red>"+guiclass.settings.me+"</font>",msg,time,day)
	  gobject.idle_add(loadchat,guiclass,guiclass.recipent)
	  #n=guiclass.chat.append(["-= Me : "+msg])
	  #update(guiclass,n)
