#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,send,sys


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
		#tworzymy słownik par - "sygnał":funkcja
		dic={
		"send": self.send,
		}
		
		self.chat=gtk.ListStore(str)
		self.chatwindow.set_model(self.chat)
		#i podpinamy go do sygnałow z glade
		self.wTree.signal_autoconnect(dic)
	#------------------------------------------------login i haslo
	
		jid = 'pybberclient@gmail.com' # @gmail.com 
		pwd   = 'pybberjabber'
		jid=xmpp.protocol.JID(jid)  
		self.cl=xmpp.Client(jid.getDomain(),debug=[])
		if self.cl.connect() == "":
			print "not connected"
			sys.exit(0) 
		if self.cl.auth(jid.getNode(),pwd) == None: 
			print "authentication failed"
			sys.exit(0)
		self.cl.send(xmpp.dispatcher.Presence(priority=5, show=None,status="Pybber test"))
	#------------------------------------------------
	
	def send(self,widget):
		send.send(self)
				
if __name__ == "__main__":

	klasa=okno()
	gtk.main()	
