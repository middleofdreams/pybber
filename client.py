#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk,gtk,gtk.glade,xmpp,sys,pango
from connection import connection
import keys
import send
from list import create_empty_list
from chatwindow import *
import webkit
from settings import *
from list import *

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
		self.clearmsg=self.wTree.get_widget("button6")
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
		"cancel":self.cancel
		}
		
		self.messages={}
		self.recipent=""
	#---------Skroty klawiszowe--------------------------------------
		
		self.message.connect("key_press_event", keys.message,self)
		self.desc.connect("key_press_event", keys.status,self)
		
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
		self.hidebtn=self.wTree.get_widget("button9")
		self.connection=connection(self)
		self.list.set_reorderable(True)
		
		self.statusentry.hide()
		self.statusbar.hide()
	#------------------------------------------elementy menu Kontakty	
	
	def adduser(self, *widget):
		self.list.hide()
		self.addform.show()
		
		
	def deluser(self, *widget):
		self.list.hide()
		self.delform.show()
		index=self.list.get_selection()
		index=index.get_selected()[1]
		index=self.listmodel.get_value(index,4)
		print index
		self.deljid.set_text(index)
		
	def edituser(self, *widget):
		self.list.hide()
		self.editform.show()
		index=self.list.get_selection()
		index=index.get_selected()[1]
		index=self.listmodel.get_value(index,4)
		print index
		self.editjid.set_text(index)
	def authorize(self, *widget):
		index=self.list.get_selection()
		index=index.get_selected()[1]
		index=self.listmodel.get_value(index,4)
		print index
		self.connection.roster.Authorize(index)
		self.connection.roster.Subscribe(index)
			
	#----------------------------------------------------------------
	
	def add(self, *widget):				#przycisk "dodaj" w formularzu
		self.list.show()				#dodania uzytkownika
		self.addform.hide()
		additem=self.addjid.get_text()
		name=self.setname.get_text()
		if name=='' or name=="": name=additem
		self.listmodel.prepend([name,'',get_show('offline'),None,additem]) 
		self.connection.roster.setItem(additem, name=name, groups=[])
		self.connection.roster.Authorize(additem)
		self.connection.roster.Subscribe(additem)
		self.addjid.set_text("")
		
	def delete(self, *widget):				#przycisk "usuń" w formularzu
		self.list.show()				#dodania uzytkownika
		self.delform.hide()
		is_deletable=False
		delitem=self.deljid.get_text()
		item = self.listmodel.get_iter_first ()
		while ( item != None ):
			if self.listmodel.get_value(item, 4)==delitem: 
				delete=item
				is_deletable=True
			item =self.listmodel.iter_next(item)
		if is_deletable: self.listmodel.remove(delete)
		self.connection.roster.delItem(delitem)
		self.connection.roster.Unauthorize(delitem)
		self.connection.roster.Unsubscribe(delitem)
		self.deljid.set_text("")
	
	def edit(self, *widget):				#przycisk "edytuj" w formularzu
		self.list.show()				#dodania uzytkownika
		self.editform.hide()
		
		is_deletable=False
		delitem=self.editjid.get_text()
		item = self.listmodel.get_iter_first ()
		while ( item != None ):
			if self.listmodel.get_value(item, 4)==delitem: 
				delete=item
				is_deletable=True
			item =self.listmodel.iter_next(item)
		if is_deletable: self.listmodel.remove(delete)
		self.connection.roster.delItem(delitem)
		self.connection.roster.Unauthorize(delitem)
		self.connection.roster.Unsubscribe(delitem)
		
		additem=self.editjid.get_text()
		name=self.editname.get_text()
		if name=='' or name=="": name=additem
		self.listmodel.prepend([name,'',get_show('offline'),None,additem]) 
		self.connection.roster.setItem(additem, name=name, groups=[])
		self.connection.roster.Authorize(additem)
		self.connection.roster.Subscribe(additem)
		self.editjid.set_text("")
	def show_hide(self, *widget):  #hide chat
		if self.recipent !="":
			self.leftwindow.hide()
			self.window.set_title("Pybber")
			self.recipent=""
			mainh=self.window.get_size()[1]
			self.window.resize(300,mainh)	
			self.window.set_position(500,500)
		else :
			self.leftwindow.show() #show chat
		
	def cancel(self, *widget):	
		self.list.show()				
		self.addform.hide()
		self.delform.hide()
		self.editform.hide()

	def clear(self, *widget):
		if self.recipent in self.messages:
			self.messages[self.recipent]=""
			loadchat(self,self.recipent)	
	def logon(self,*widget):
		
		jid=self.login.get_text()
		pwd=self.passwd.get_text()
		self.connection.connect_init(self,jid,pwd)
		self.settings.saveacc(self)
		self.loginbox.hide()
		
	#------------------------------------------------
	def changedata(self, *widget):
		self.toolong.hide()
		self.loginbox.show()
		self.not_connected.hide()
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
		
	def savesettings(self,widget):
		self.settings.save(self)
			
	def closesettings(self,widget):
		self.wTree.get_widget('frame1').hide()
	def opensettings(self,widget):
		self.wTree.get_widget('frame1').show()
		self.wTree.get_widget('combobox2').set_active(self.settings.show)
		self.wTree.get_widget('entry5').set_text(self.settings.status)
				
if __name__ == "__main__":
	gtk.gdk.threads_init()
	klasa=okno()
	gtk.main()	
