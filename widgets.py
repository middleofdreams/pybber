#!/usr/bin/python
# -*- coding: utf-8 -*-
import gtk
import keys
from list import *
import webkit
from settings import *

def assignwidgets(self):
		self.window.set_icon_from_file("icons/pybber.png")
		self.menu=self.wTree.get_widget("menubar1")
		self.list=self.wTree.get_widget("treeview1")
		self.statusbar=self.wTree.get_widget("combobox1")
		self.button=self.wTree.get_widget("button1")
		self.message=self.wTree.get_widget("textview1")
		self.archivelist=self.wTree.get_widget("treeview2")
		self.archivewindow=self.wTree.get_widget("vbox9")
		self.archivescroll=self.wTree.get_widget("scrolledwindow3")
		self.progress=self.wTree.get_widget("progressbar1")
		self.desc=self.wTree.get_widget("entry2")
		self.toolong=self.wTree.get_widget("vbox1")
		self.not_connected=self.wTree.get_widget("vbox4")
		self.clearmsg=self.wTree.get_widget("button6")
		self.jidlabel=self.wTree.get_widget("label13")
		self.statusentry=self.wTree.get_widget("entry2")
		
		self.loginbox=self.wTree.get_widget("vbox5")
		self.login=self.wTree.get_widget("entry4")
		self.passwd=self.wTree.get_widget("entry3")
		self.logonbtn=self.wTree.get_widget("button5")
		self.addform=self.wTree.get_widget("table1")
		self.delform=self.wTree.get_widget("table2")
		self.editform=self.wTree.get_widget("table3")
		self.addjid=self.wTree.get_widget("entry5")
		self.deljid=self.wTree.get_widget("entry7")
		self.editjid=self.wTree.get_widget("entry9")
		self.setname=self.wTree.get_widget("entry6")
		self.editname=self.wTree.get_widget("entry10")
		#ustawienie statusow z ikonami
		self.statuslist=gtk.ListStore(str,gtk.gdk.Pixbuf)
		self.statusbar.set_model(self.statuslist)
		self.statuslist.append(["Dostępny",gtk.gdk.pixbuf_new_from_file("icons/online.png")])
		self.statuslist.append(["Zaraz wracam",gtk.gdk.pixbuf_new_from_file("icons/away.png")])
		self.statuslist.append(["Wrócę później",gtk.gdk.pixbuf_new_from_file("icons/extended-away.png")])
		self.statuslist.append(["Nie przeszkadzać",gtk.gdk.pixbuf_new_from_file("icons/busy.png")])
		self.statuslist.append(["Chcę pogadać",gtk.gdk.pixbuf_new_from_file("icons/chat.png")])
		self.statuslist.append(["Niewidoczny",gtk.gdk.pixbuf_new_from_file("icons/invisible.png")])
		
		self.contactpopup=self.wTree.get_widget("menu4")
		self.iconpopup=self.wTree.get_widget("menu5")
		
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
		"chdesc": self.chstatus,
		"chstatus": self.chstatus,
		"reconnect": self.reconnect,
		"reconnect2": self.reconnect2,
		"hidewarn": self.hidewarn,
		"resize": self.resize,
		"logon": self.logon,
		"clear": self.clear,
		"changedata":self.changedata,
		"savesettings":self.savesettings,
		"closesettings":self.closesettings,
		"opensettings":self.opensettings,
		"show_hide":self.show_hide,
		"authorize":self.authorize,
		"adduser":self.adduser,
		"deluser":self.deluser,
		"edituser":self.edituser,
		"close":self.close,
		"add":self.add,
		"delete":self.delete,
		"edit":self.edit,
		"cancel":self.cancel,
		"contactpopup": self.contactmenu,
		"set_online":self.set_online,
		"set_away":self.set_away,
		"set_xa":self.set_xa,
		"set_dnd":self.set_dnd,
		"set_chat":self.set_chat,
		"set_invisible":self.set_invisible,
		"activate":self.activate,
		"chatfocus":self.chatfocus,
		"notification":self.notification,
		"archive":self.archive,
		"closearchive":self.closearchive
			}
		
			#---------Skroty klawiszowe--------------------------------------
		self.message.connect("key_press_event", keys.message,self)
		self.message.get_buffer().connect_after("insert-text", keys.msgbuffer)
		self.desc.connect("key_press_event", keys.status,self)
		self.list.connect("key_press_event", keys.list,self)
	#---Stworzenie modelu dla wyswietlania rozmow----------------------
		create_empty_list(self)
		self.chatwindow=self.wTree.get_widget("scrolledwindow1")
		self.chat=webkit.WebView()
		self.wTree.get_widget("scrolledwindow1").add(self.chat)
		self.chat.show()
		self.wTree.signal_autoconnect(dic)
		self.chat.connect("load-finished", self.loadFinished)
		self.settings=settings()
		self.settings.loadprefs(self)
		self.leftwindow=self.wTree.get_widget("vbox3")
		self.chat.connect("key_press_event", keys.chat,self)
		self.chat.connect("new-window-policy-decision-requested",self.link)
		self.hidebtn=self.wTree.get_widget("button9")
	#------------------------------------------elementy menu Kontakty
		self.list.set_reorderable(True)
		self.window.connect("drag-end", self.resize)
		self.window.connect("drag-drop", self.resize)
def createstatusicon(mainclass):	
 
		mainclass.staticon = gtk.StatusIcon() 
		mainclass.staticon.set_from_file("icons/pybber.png") 
		mainclass.staticon.set_blinking(False) 
		mainclass.staticon.set_tooltip("Pybber")
		mainclass.staticon.connect("activate", mainclass.activate) 
		mainclass.staticon.connect("popup_menu",mainclass.iconmenu, mainclass.iconpopup)
		
		mainclass.staticon.set_visible(True)
		
def contactmenuactivate(self):
		self.list.connect("button_press_event", self.contactmenu, self.contactpopup) 
		self.window.connect("button_press_event", self.chatfocus)
