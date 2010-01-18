#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,sys,pango,os,time,pynotify
from connection import *
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
			self.window.connect('delete-event', self.icohide)
		mainh=self.window.get_size()[1]
		self.window.resize(300	,mainh)
		self.window.set_default_size(300, mainh)
		self.window.move(int(gtk.gdk.screen_width()*0.7),int(gtk.gdk.screen_height(	)*0.2))
		#po zamknięciu okna - kończymy program
		
		self.window.set_title("Pybber")
		
		#pobranie obiektow z glade i przypisywanie ich do zmiennych:
		self.messages={}
		self.recipent=""
		assignwidgets(self)
		createstatusicon(self)
		self.connection=connection(self)
		self.list.set_reorderable(True)
		self.statusentry.hide()
		self.statusbar.hide()
		self.hidden=False
		self.posx,self.posy=self.window.get_position()
		pynotify.init("Pybber")
		
		
if __name__ == "__main__":
	gtk.gdk.threads_init()
	klasa=okno()
	gtk.main()	
