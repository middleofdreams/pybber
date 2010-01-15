#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,sys,pango,os,time
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
			self.window.connect("destroy",self.close)
		mainh=self.window.get_size()[1]
		self.window.resize(300,mainh)
		self.window.set_default_size(300, mainh)
		self.window.move(int(gtk.gdk.screen_width()*0.7),int(gtk.gdk.screen_height()*0.2))
		
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
		
		self.list.add_events(gtk.gdk.BUTTON_PRESS_MASK)

	def button_clicked(widget, event):
	 # which button was clicked?
		if event.button == 1:
			print "left click"
		elif event.button == 2:
			print "middle click"
		elif event.button == 3:
			print "right click"
	
	def iconmenu(self,widget, button, time, test = None):
		if button == 3:
			if test:
				print "A"
				self.iconpopup.show_all()
				self.iconpopup.popup(None, None, None, 3, time)
				

	
	def contactmenu(self, treeview, event):
		if event.button == 3:
			print "AA"
			x = int(event.x)
			y = int(event.y)
			time = event.time
			pthinfo = treeview.get_path_at_pos(x, y)
			if pthinfo is not None:
				path, col, cellx, celly = pthinfo
				treeview.grab_focus()
				treeview.set_cursor( path, col, 0)
				self.contactpopup.popup( None, None, None, 3, time)
				return True
				#self.contactpopup.show_all()
				#self.contactpopup.popup( None, None, None, 3, time)
         
				

if __name__ == "__main__":
	gtk.gdk.threads_init()
	klasa=okno()
	gtk.main()	
