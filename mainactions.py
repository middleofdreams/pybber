#!/usr/bin/python
# -*- coding: utf-8 -*-
from listmanage import *
import gtk,sys,time
from send import *
from connection import *
def show_hide(self, *widget):  #hide chat
	
	mainh=self.window.get_size()[1]	
	
	x,y=self.window.get_position()
	x=(x+400)
	self.recipent=""
	self.window.set_title("Pybber")
	self.window.set_gravity(gtk.gdk.GRAVITY_SOUTH_EAST)
	self.leftwindow.hide()
	#self.window.reshow_with_initial_size()
	self.window.resize(300,mainh)
	#self.window.move(x,y)


		
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
	self.jidlabel.set_label(jid)	
#------------------------------------------------
def changedata(self, *widget):
	self.toolong.hide()
	self.loginbox.show()
	self.not_connected.hide()
def send(self,*widget):
	sendmsg(self)
def chdesc(self,*widget):
	desc=self.desc.get_text()
	index=self.statusbar.get_active()
	self.connection.set_status(index,desc)
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
def icohide(self, event,widget):
	self.window.hide()
	return True
	window.connect('delete-event', hide_window)
def loadFinished(self,a,b):
	pos=self.chatwindow.get_vadjustment()
	newpos=pos.get_upper()
	pos.set_value(newpos)
	self.chatwindow.set_vadjustment(pos)  
	
def savesettings(self,widget):
	self.settings.save(self)
		
def closesettings(self,widget):
	self.window.set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
	self.wTree.get_widget('frame1').hide()
	mainh=self.window.get_size()[1]	
	self.window.resize(300,mainh)
def opensettings(self,widget):
	self.window.set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
	self.wTree.get_widget('frame1').show()
	self.wTree.get_widget('combobox2').set_active(self.settings.show)
	self.wTree.get_widget('entry8').set_text(self.settings.status)
	self.wTree.get_widget('entry11').set_text(self.settings.me)
def activate(self,widget):
	if self.window.is_active():
		self.window.present()
		self.pos=self.window.get_position()
		self.window.hide()
		print self.pos
	else:
		
		self.window.show()
		self.window.move(self.pos[0],self.pos[1])
		self.window.present()
		

	
def iconmenu(self,widget, button, time, test = None):
	if button == 3:
		if test:
			print "A"
			self.iconpopup.show_all()
			self.iconpopup.popup(None, None, None, 3, time)
			


def contactmenu(self, treeview, event):
	if event.button == 3:
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
         
