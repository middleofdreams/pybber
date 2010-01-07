# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp

def send(guiclass):
  msg=guiclass.message.get_text()
  guiclass.message.set_text("")
 # msg=str("ME:"+msg)
  print msg

  for i in range(100):  guiclass.cl.send(xmpp.Message("must40@gmail.com" ,msg))
  guiclass.chat.append(msg)
	
