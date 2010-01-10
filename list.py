# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk

def create_empty_list(guiclass):
	guiclass.listmodel=gtk.ListStore(str)
	guiclass.list.set_model(guiclass.listmodel)
	guiclass.lrenderer=gtk.CellRendererText()
	guiclass.lcolumn=gtk.TreeViewColumn("Konktakty:",guiclass.lrenderer, text=0)
	guiclass.list.append_column(guiclass.lcolumn)

def update_list(guiclass,list):
	for i in list:
		guiclass.listmodel.append([i])
		
