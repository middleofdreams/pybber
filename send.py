# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp
from chatwindow import *

def send(guiclass):
  msg=guiclass.message.get_text()
  guiclass.message.set_text("")
 # msg=str("ME:"+msg)
  if msg!="":
	  #for i in range(100): 
	  guiclass.connection.send(msg)
	  savechat(guiclass,guiclass.recipent,"Me",msg)
	  n=guiclass.chat.append(["-= Me : "+msg])
	  update(guiclass,n)
