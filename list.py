# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp
from chatwindow import *

def on_activated(widget, row, col,guiclass):
	'''zmienia aktualnego rozmowce'''  
	model = widget.get_model()
	text = model[row][4]
	if guiclass.window.get_title()=="Pybber":
		x1,y1=guiclass.window.get_position()
		guiclass.window.move(x1-400,y1)
		guiclass.leftwindow.show()
		
		
	guiclass.window.set_title("Rozmowa z "+model[row][0]+" ("+text+")")
	guiclass.recipent=text

	
	loadchat(guiclass,text)
	show_back(guiclass,model[row])

	 
def create_empty_list(guiclass):
	'''tworzy pusta liste'''
	guiclass.listmodel=gtk.ListStore(str,str,gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,str)
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
	'''aktualizuje zmieniajace sie wpisy'''
	
	#sprawdzanie kto sie zmienil 
	jid=pres.getFrom()
	nick=pres.getFrom().getStripped()
	
	
	status=guiclass.connection.roster.getStatus(jid.__str__())	
	priority= guiclass.connection.roster.getPriority(jid.__str__())
	
	#sprawdzenie czy zalogowany
	if priority==None:
		show='offline'
	else:	
		show=guiclass.connection.roster.getShow(jid.__str__())		
	
	#przypisanie kontaktow do tymczasowej listy
	cats = list ()
	item = guiclass.listmodel.get_iter_first ()
	while ( item != None ):
		cats.append (guiclass.listmodel.get_value (item, 4))
		item = guiclass.listmodel.iter_next(item)
	#sprawdzenie czy kontakt znajduje sie na liscie	
	if not nick in cats:
		guiclass.listmodel.append([nick,status,get_show(show),None,nick])
	else:
	#jesli tak - aktualizuj wpis
		item = guiclass.listmodel.get_iter_first ()
		while ( guiclass.listmodel.get_value(item,4)!=nick):
			cats.append (guiclass.listmodel.get_value (item, 4))
			item = guiclass.listmodel.iter_next(item)
		guiclass.listmodel.set_value(item,1,status)
		if guiclass.listmodel.get_value(item,3)!=None:
			guiclass.listmodel.set_value(item,3,get_show(show))
		else:
			guiclass.listmodel.set_value(item,2,get_show(show))


def get_all(guiclass,list):	
	'''pobiera wszystkie kontakty z rostera'''
	for i in list:		
		status=guiclass.connection.roster.getStatus(str(xmpp.protocol.JID(jid=i)))	
		show=guiclass.connection.roster.getShow(str(xmpp.protocol.JID(jid=i)))	
		name=guiclass.connection.roster.getName(str(xmpp.protocol.JID(jid=i)))
		#domyslne oznaczanie kontaktow jako niedostepnych
		if name==None: name=i
		guiclass.listmodel.append([name,status,get_show('offline'),None,i])
		
def get_show(show):
	'''pobiera obrazek statusu'''
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

def is_typing(guiclass,nick):
	show=gtk.gdk.pixbuf_new_from_file("icons/typing.png")

	cats = list()
	item = guiclass.listmodel.get_iter_first ()
	while ( item != None ):
		cats.append (guiclass.listmodel.get_value (item, 4))
		item = guiclass.listmodel.iter_next(item)
	#sprawdzenie czy kontakt znajduje sie na liscie	
	if not nick in cats:
		guiclass.listmodel.append([nick,status,show,nick])
	else:
	#jesli tak - aktualizuj wpis
		item = guiclass.listmodel.get_iter_first ()
		while ( guiclass.listmodel.get_value(item,4)!=nick):
			cats.append (guiclass.listmodel.get_value (item, 4))
			item = guiclass.listmodel.iter_next(item)
	pshow=guiclass.listmodel.get_value(item,2)
	guiclass.listmodel.set_value(item,3,pshow)
	guiclass.listmodel.set_value(item,2,show)

def show_back(guiclass,item):
	if item[3]!=None:
		item[2]=item[3]
		
		item[3]=None
