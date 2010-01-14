#!/usr/bin/python
# -*- coding: utf-8 -*-
def adduser(self, *widget):
	self.list.hide()
	self.addform.show()
	
	
def deluser(self, *widget):
	index=self.list.get_selection()
	index=index.get_selected()[1]
	index=self.listmodel.get_value(index,4)
	print index
	if index > -1:
		self.deljid.set_text(index)
	self.list.hide()
	self.delform.show()
	
def edituser(self, *widget):
	self.list.hide()
	self.editform.show()
	edititem=self.editjid.get_text()
def authorize(self, *widget):
	pass
		
#----------------------------------------------------------------

def add(self, *widget):				#przycisk "dodaj" w formularzu
	self.list.show()				#dodania uzytkownika
	
	additem=self.addjid.get_text()			
	name=self.setname.get_text()
	if name=='' or name=="": name=additem
	self.addform.hide()
	
	self.listmodel.prepend([name,'',get_show('offline'),None,additem])
	if name==additem:
		self.connection.roster.setItem(additem, name=None, groups=[])
	else:
		self.connection.roster.setItem(additem, name=name, groups=[])
	self.connection.roster.Authorize(additem)
	self.connection.roster.Subscribe(additem)
def delete(self, *widget):
	
	
	is_deletable=False				#przycisk "usuń" w formularzu
	self.list.show()				#dodania uzytkownika
	self.delform.hide()
	delitem=self.deljid.get_text()
	item = self.listmodel.get_iter_first ()
	while ( item != None ):
		if self.listmodel.get_value(item, 4)==delitem: 
			delete=item
			is_deletable=True
		item =self.listmodel.iter_next(item)
	if is_deletable: 
		self.listmodel.remove(delete)
		self.connection.roster.delItem(delitem)
		self.connection.roster.Unauthorize(delitem)
		self.connection.roster.Unsubscribe(delitem)
		self.deljid.set_text("")
	
def edit(self, *widget):				#przycisk "edytuj" w formularzu
	self.list.show()				#dodania uzytkownika
	self.editform.hide()
	edititem=self.editjid.get_text()
	name=self.editname.get_text()
	self.connection.roster.setItem(edititem, name=name, groups=[])
