#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,sys,pango
from connection import connection
import keys
import send

from chatwindow import *
from widgets import *


class okno:
	from mainactions import *
	def __init__(self):
		self.gladefile = "client.glade"
		self.wTree = gtk.glade.XML(self.gladefile) 
		# pobieramy główne okno
		self.window = self.wTree.get_widget("window1")
		self.window.show()
		#wyświetlamy głowne okno
		if (self.window):
			self.window.connect("destroy",self.close)
		#po zamknięciu okna - kończymy program
		
		self.window.set_title("Pybber")
		
		#pobranie obiektow z glade i przypisywanie ich do zmiennych:
		

		self.messages={}
		self.recipent=""
		assignwidgets(self)
		self.connection=connection(self)

		self.list.set_reorderable(True)
		
		self.statusentry.hide()
		self.statusbar.hide()


if __name__ == "__main__":
	gtk.gdk.threads_init()
	klasa=okno()
	gtk.main()	
