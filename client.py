#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,sys,pango
from connection import connection
import keys
import send

class okno:
	def __init__(self):
		self.gladefile = "client.glade"
		self.wTree = gtk.glade.XML(self.gladefile) 
		# pobieramy główne okno
		self.window = self.wTree.get_widget("window1")
		self.window.show()
		#wyświetlamy głowne okno
		if (self.window):
			self.window.connect("destroy",gtk.main_quit)
		#po zamknięciu okna - kończymy program
		
		#pobranie obiektow z glade i przypisywanie ich do zmiennych:
		
		self.menu=self.wTree.get_widget("menubar1")
		self.list=self.wTree.get_widget("treeview1")
		self.statusbar=self.wTree.get_widget("combobox1")
		self.button=self.wTree.get_widget("button1")
		self.message=self.wTree.get_widget("entry1")
		self.chatwindow=self.wTree.get_widget("treeview2")
		self.progress=self.wTree.get_widget("progressbar1")
		self.desc=self.wTree.get_widget("entry2")
		
		self.desc=login.wTree.get_widget("entry4")
		self.desc=passwd.wTree.get_widget("entry3")
		
		
		#ustawienie statusow
		self.statuslist=gtk.ListStore(str)
		self.statusbar.set_model(self.statuslist)
		self.statuslist.append(["Dostepny"])
		self.statuslist.append(["Zaraz wracam"])
		self.statuslist.append(["Wrócę później"])
		self.statuslist.append(["Nie przeszkadzać"])
		self.statuslist.append(["Chcę pogadać"])
		self.statuslist.append(["Niewidoczny"])
		
		#wyswietlanie statusow
		cell = gtk.CellRendererText()
		self.statusbar.pack_start(cell)
		self.statusbar.add_attribute(cell, 'text', 0)
		
		
		#sygnaly
		dic={
		"send": self.send,
		"chdesc": self.chdesc,
		"chstatus": self.chstatus
		}
		
	#---------Skroty klawiszowe--------------------------------------
		
		self.message.connect("key_press_event", keys.message,self)
		self.desc.connect("key_press_event", keys.status,self)
	
	#---Stworzenie modelu dla wyswietlania rozmow----------------------
	
		self.chat=gtk.ListStore(str)
		self.chatwindow.set_model(self.chat)
		renderer=gtk.CellRendererText()
		self.column=gtk.TreeViewColumn("Rozmowa z ...",renderer, text=0)
		self.chatwindow.append_column(self.column)
		#self.column.set_title("test")
		self.wTree.signal_autoconnect(dic)
	
	#------Połączenie z serwerem XMPP----------------
		
		self.connection=connection(self)
	#------------------------------------------------
	
	def send(self,*widget):
		send.send(self)
	def chdesc(self,*widget):
		desc=self.desc.get_text()
		self.connection.set_desc(desc)
	def chstatus(self,widget):
		desc=self.desc.get_text()
		index=self.statusbar.get_active()
		self.connection.set_status(index,desc)

				
if __name__ == "__main__":
	gtk.gdk.threads_init()
	klasa=okno()
	gtk.main()	
