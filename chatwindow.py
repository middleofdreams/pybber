# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk
#-----------aktualizacja szerokosci wrappera i scrolldown
def update(guiclass,n):
	try:
		guiclass.renderer.props.wrap_width = int(guiclass.column.get_width())-int(10)
	except:
		pass
	n=guiclass.chat.get_path(n)
	guiclass.chatwindow.scroll_to_cell(n) 

def savechat(guiclass,recipent,user,chat):
	text="-= "+user+": "+chat
	if recipent in guiclass.messages: 
		guiclass.messages[recipent].append(text)
	else : guiclass.messages[recipent]=[text]

def loadchat(guiclass,recipent):
	if recipent in guiclass.messages:
			for text in guiclass.messages[recipent]: n=guiclass.chat.append([text])
			update(guiclass,n)
