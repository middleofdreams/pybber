#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,sys,pango
from connection import connection
import keys
import send
from list import create_empty_list
import webkit

class okno:
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
		
		self.menu=self.wTree.get_widget("menubar1")
		self.list=self.wTree.get_widget("treeview1")
		self.statusbar=self.wTree.get_widget("combobox1")
		self.button=self.wTree.get_widget("button1")
		self.message=self.wTree.get_widget("entry1")
		#self.chatwindow=self.wTree.get_widget("treeview2")
		self.progress=self.wTree.get_widget("progressbar1")
		self.desc=self.wTree.get_widget("entry2")
		self.toolong=self.wTree.get_widget("vbox1")
		self.not_connected=self.wTree.get_widget("vbox4")

		
		self.login=self.wTree.get_widget("entry4")
		self.passwd=self.wTree.get_widget("entry3")
		self.logonbtn=self.wTree.get_widget("button5")
		
		#ustawienie statusow z ikonami
		self.statuslist=gtk.ListStore(str,gtk.gdk.Pixbuf)
		self.statusbar.set_model(self.statuslist)
		self.statuslist.append(["Dostepny",gtk.gdk.pixbuf_new_from_file("icons/online.png")])
		self.statuslist.append(["Zaraz wracam",gtk.gdk.pixbuf_new_from_file("icons/away.png")])
		self.statuslist.append(["Wrócę później",gtk.gdk.pixbuf_new_from_file("icons/extended-away.png")])
		self.statuslist.append(["Nie przeszkadzać",gtk.gdk.pixbuf_new_from_file("icons/busy.png")])
		self.statuslist.append(["Chcę pogadać",gtk.gdk.pixbuf_new_from_file("icons/chat.png")])
		self.statuslist.append(["Niewidoczny",gtk.gdk.pixbuf_new_from_file("icons/invisible.png")])
		
		#wyswietlanie statusow
		cell = gtk.CellRendererText()
		cell2=gtk.CellRendererPixbuf()
		cell2.set_fixed_size(24,24)
		self.statusbar.pack_start(cell2,expand=False)
		self.statusbar.pack_start(cell)
		self.statusbar.add_attribute(cell2, 'pixbuf', 1)
		self.statusbar.add_attribute(cell, 'text', 0)
		
		
		#sygnaly
		dic={
		"send": self.send,
		"chdesc": self.chdesc,
		"chstatus": self.chstatus,
		"reconnect": self.reconnect,
		"reconnect2": self.reconnect2,
		"hidewarn": self.hidewarn,
		"resize": self.resize,
		"logon": self.logon
		}
		
		self.messages={}
		self.recipent=""
	#---------Skroty klawiszowe--------------------------------------
		
		self.message.connect("key_press_event", keys.message,self)
		self.desc.connect("key_press_event", keys.status,self)
		
	#---Stworzenie modelu dla wyswietlania rozmow----------------------
		create_empty_list(self)
		#self.chat=gtk.ListStore(str)
		self.chatwindow=self.wTree.get_widget("scrolledwindow1")
		#self.renderer=gtk.CellRendererText()
		#self.renderer.props.wrap_width = 300
		#self.renderer.props.wrap_mode = gtk.WRAP_WORD
		#self.column=gtk.TreeViewColumn("Rozmowa z ...",self.renderer, text=0)
		#self.chatwindow.append_column(self.column)
		#self.column.set_title("test")
		self.chat=webkit.WebView()
		self.wTree.get_widget("scrolledwindow1").add(self.chat)
		self.chat.show()
		self.wTree.signal_autoconnect(dic)
		self.chat.connect("load-finished", self.loadFinished)
	#------Połączenie z serwerem XMPP----------------
		
	def logon(self,*widget):
		jid=self.login.get_text()
		pwd=self.passwd.get_text()
		self.connection=connection(self,jid,pwd)
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
		
	def hidewarn(self,widget):
		self.toolong.hide()
	def reconnect(self,widget):
		self.connection.reconnect()
	def reconnect2(self,widget):
		self.connection.reconnect2()
	def resize(self,widget):
		pass
		#  self.renderer.props.wrap_width = int(self.column.get_width())-int(10)
	def close(self,*widget):
		self.connection.cl=None
		self.connection=None
		gtk.main_quit()
		sys.exit(0)
		
	def loadFinished(self,a,b):
		pos=self.chatwindow.get_vadjustment()
		newpos=pos.get_upper()
		pos.set_value(newpos)
		self.chatwindow.set_vadjustment(pos)  
				
if __name__ == "__main__":
	gtk.gdk.threads_init()
	klasa=okno()
	gtk.main()	
