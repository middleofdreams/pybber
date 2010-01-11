# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp

def on_activated(widget, row, col,guiclass):       
     model = widget.get_model()
     text = model[row][0]
     guiclass.column.set_title("Rozmowa z "+text)
     guiclass.recipent=text
     guiclass.wTree.get_widget("vbox3").show()
     
	 
	 
def create_empty_list(guiclass):
	guiclass.listmodel=gtk.ListStore(str,str,gtk.gdk.Pixbuf)
	guiclass.list.set_model(guiclass.listmodel)
	guiclass.lrenderer=gtk.CellRendererText()
	guiclass.lcolumn=gtk.TreeViewColumn("Kontakty:",guiclass.lrenderer, text=0)
	guiclass.lcolumn2=gtk.TreeViewColumn("Opisy",guiclass.lrenderer, text=1)
	guiclass.lcolumn3=gtk.TreeViewColumn("Statusy",gtk.CellRendererPixbuf(), pixbuf=2)
	guiclass.list.append_column(guiclass.lcolumn3)
	guiclass.list.append_column(guiclass.lcolumn)
	guiclass.list.append_column(guiclass.lcolumn2)
	guiclass.list.set_headers_visible(0)
	guiclass.list.connect("row-activated", on_activated, guiclass)
	
def update_list(guiclass,sess,pres):
	jid=pres.getFrom()
	nick=pres.getFrom().getStripped()
	print nick
	cats = list ()
	item = guiclass.listmodel.get_iter_first ()
	status=guiclass.connection.roster.getStatus(jid.__str__())	
	priority= guiclass.connection.roster.getPriority(jid.__str__())
	if priority==None:
		show='offline'
	else:	
		show=guiclass.connection.roster.getShow(jid.__str__())		

	while ( item != None ):
		cats.append (guiclass.listmodel.get_value (item, 0))
		item = guiclass.listmodel.iter_next(item)
		
	if not nick in cats:
		guiclass.listmodel.append([nick,status,show])
	else:
		item = guiclass.listmodel.get_iter_first ()
		while ( guiclass.listmodel.get_value(item,0)!=nick):
			cats.append (guiclass.listmodel.get_value (item, 0))
			item = guiclass.listmodel.iter_next(item)
		guiclass.listmodel.set_value(item,1,status)
		guiclass.listmodel.set_value(item,2,get_show(show))


def get_all(guiclass,list):	
	for i in list:		
		status=guiclass.connection.roster.getStatus(str(xmpp.protocol.JID(jid=i)))	
		show=guiclass.connection.roster.getShow(str(xmpp.protocol.JID(jid=i)))	
		guiclass.listmodel.append([i,status,get_show('offline')])
		
def get_show(show):
	if show==None:
		show=gtk.gdk.pixbuf_new_from_file("icons/online.png")
	if show=="dnd":
		show=gtk.gdk.pixbuf_new_from_file("icons/busy.png")
	if show=="chat":
		show=gtk.gdk.pixbuf_new_from_file("icons/chat.png")	
	if show=="away":
		show=gtk.gdk.pixbuf_new_from_file("icons/away.png")
	if show=="xa":
		show=gtk.gdk.pixbuf_new_from_file("icons/extended-away.png")
	if show=='offline':
		show=gtk.gdk.pixbuf_new_from_file("icons/offline.png")
	return show
