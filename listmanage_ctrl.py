# -*- coding: utf-8 -*-
from gtkmvc import Controller
from gtkmvc.adapters import Adapter
from listhelpers import *

class ListCtrl (Controller):
    """Handles signal processing, and keeps alignment of model and
    view"""
    def __init__(self, model, view):  
        Controller.__init__(self, model, view)  
        return  

    def adduser(self, *widget):
        self.view.list_showform("add")
        
        
    def deluser(self, *widget):
        index=self.view['list'].get_selection()
        index=index.get_selected()[1]
        jid=self.view['listmodel'].get_value(index,4)
        self.view.list_showform("del",True,jid,None)

        
    def edituser(self, *widget):
        index=self.view['list'].get_selection()
        index=index.get_selected()[1]
        jid=self.view['listmodel'].get_value(index,4)
        name=self.view['listmodel'].get_value(index,0)
        self.edited=jid
        if name==jid: name=None
        self.view.list_showform("edit",True,jid,name)
    def authorize(self, *widget):
        index=self.list.get_selection()
        index=index.get_selected()[1]
        index=self.listmodel.get_value(index,4)
        self.connection.roster.Authorize(index)
        self.connection.roster.Subscribe(index)
            
    
    def add(self, *widget):                #przycisk "dodaj" w formularzu
        additem=self.view['addjid'].get_text()
        name=self.view['addname'].get_text()
        if name=='' or name=="": name=additem
        self.view['listmodel'].prepend([name,'',get_show('offline'),None,additem,0]) 
        self.model.connection.roster.setItem(additem, name=name, groups=[])
        self.model.connection.roster.Authorize(additem)
        self.model.connection.roster.Subscribe(additem)
        self.view.list_hideform("add")
        
    def delete(self, *widget):                #przycisk "usuￅﾄ" w formularzu
        is_deletable=False
        delitem=self.view['deljid'].get_text()
        item = self.view['listmodel'].get_iter_first ()
        while ( item != None ):
            if self.view['listmodel'].get_value(item, 4)==delitem: 
                delete=item
                is_deletable=True
            item =self.view['listmodel'].iter_next(item)
        if is_deletable: self.view['listmodel'].remove(delete)
        self.model.connection.roster.delItem(delitem)
        self.model.connection.roster.Unauthorize(delitem)
        self.model.connection.roster.Unsubscribe(delitem)
        self.view.list_hideform("del")
    
    def edit(self, *widget):                #przycisk "edytuj" w formularzu
        
        
        is_editable=False
        olditem=self.edited
        item = self.view['listmodel'].get_iter_first ()
        while ( item != None ):
            if self.view['listmodel'].get_value(item, 4)==olditem: 
                edit=item
                is_deletable=True
            item =self.view['listmodel'].iter_next(item)
        
        newitem=self.view['editjid'].get_text()
        name=self.view['editname'].get_text()
        if name=='' or name=="": name=newitem
        self.view['listmodel'].set_value(edit,0,name)
        if newitem!=olditem:
            self.view['listmodel'].set_value(edit,4,newitem)
            self.view['listmodel'].set_value(edit,2,get_show('offline'))
            self.view['listmodel'].set_value(edit,1,'')

        self.model.connection.roster.delItem(olditem)
        self.model.connection.roster.setItem(newitem, name=name, groups=[])
        self.model.connection.roster.Authorize(newitem)
        self.model.connection.roster.Subscribe(newitem)
        self.edit=""
        self.view.list_hideform("edit")
        
    def cancel(self, *widget):    
        self.view.list_hideform("del")
        self.view.list_hideform("add")
        self.view.list_hideform("edit") 
        self.edit=""  
