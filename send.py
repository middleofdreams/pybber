# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp

def send(guiclass):
  msg=guiclass.message.get_text()
  guiclass.message.set_text("")
 # msg=str("ME:"+msg)
	
  #for i in range(100): 
  guiclass.connection.send(msg)
  guiclass.chat.append(["-= Me : "+msg])
  guiclass.renderer.props.wrap_width = int(guiclass.column.get_width())-int(10)
