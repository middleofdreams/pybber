# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,time
from chatwindow import *

def sendmsg(guiclass):
  msg=guiclass.message.get_text()
  guiclass.message.set_text("")
 # msg=str("ME:"+msg)
  if msg!="":
	  guiclass.connection.send(msg)
		
	  savechat(guiclass,guiclass.recipent,"<font color=red>"+guiclass.settings.me+"</font>",msg)
	  loadchat(guiclass,guiclass.recipent)
	  #n=guiclass.chat.append(["-= Me : "+msg])
	  #update(guiclass,n)
