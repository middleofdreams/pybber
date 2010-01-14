#!/usr/bin/python
# -*- coding: utf-8 -*-
from listmanage import *
import gtk,sys
from send import *
def show_hide(self, *widget):  #hide chat
	if self.recipent !="":
		self.leftwindow.hide()
		self.recipent=""
		mainh=self.window.get_size()[1]
		self.window.resize(300,mainh)	
	else :
		self.leftwindow.show() #show chat
		
		
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
	sendmsg(self)
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
			
