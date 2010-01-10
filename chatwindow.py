# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk
#-----------aktualizacja szerokosci wrappera i scrolldown
def update(guiclass,n):
	guiclass.renderer.props.wrap_width = int(guiclass.column.get_width())-int(10)
	n=guiclass.chat.get_path(n)
	guiclass.chatwindow.scroll_to_cell(n) 
