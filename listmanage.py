#!/usr/bin/python
# -*- coding: utf-8 -*-

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
	
def cancel(self, *widget):	
	self.list.show()				
	self.addform.hide()
	self.delform.hide()
	self.editform.hide()
