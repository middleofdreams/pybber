#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,send,sys
from connection import connection

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
		self.statusbar=self.wTree.get_widget("comboboxentry1")
		self.button=self.wTree.get_widget("button1")
		self.message=self.wTree.get_widget("entry1")
		self.chatwindow=self.wTree.get_widget("treeview2")
		self.progress=self.wTree.get_widget("progressbar1")
		#tworzymy słownik par - "sygnał":funkcja
		dic={
		"send": self.send,
		}
		
		self.chat=gtk.ListStore(str)
		self.chatwindow.set_model(self.chat)
		renderer=gtk.CellRendererText()
		self.column=gtk.TreeViewColumn("Rozmowa z ...",renderer, text=0)
		self.chatwindow.append_column(self.column)
		#self.column.set_title("test")
		self.wTree.signal_autoconnect(dic)
	#------------------------------------------------login i haslo
		
		self.connection=connection(self)
		
			#------------------------------------------------
	
	def send(self,widget):
		send.send(self)
				
if __name__ == "__main__":
	gtk.gdk.threads_init()
	klasa=okno()
	gtk.main()	
