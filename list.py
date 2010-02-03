import gtk,xmpp,gobject
from listhelpers import *

def create_empty_list(view):
    '''tworzy pusta liste'''
    
    view['listmodel']=gtk.ListStore(str,str,gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,str,int)
    view['list'].set_model(view['listmodel'])
    lrender=gtk.CellRendererText()
    pixrender=gtk.CellRendererPixbuf()
    strender=gtk.CellRendererText() 
    pixrender.set_property('cell-background',"#F1FAB4")
    lcolumn=gtk.TreeViewColumn("Kontakty:")
    lcolumn.pack_start(lrender)
    lcolumn.pack_start(strender)
    lcolumn.add_attribute(lrender,'markup',0)
    lcolumn.add_attribute(strender,'markup',1)
    lcolumn3=gtk.TreeViewColumn("Statusy",pixrender, pixbuf=2)
    view['list'].append_column(lcolumn3)
    view['list'].append_column(lcolumn)
    view['list'].set_headers_visible(0)
    view['listmodel'].set_sort_column_id(0,gtk.SORT_ASCENDING)
    view['listmodel'].set_sort_column_id(5,gtk.SORT_DESCENDING)

def get_all(list,widget,roster):    
    '''pobiera wszystkie kontakty z rostera'''
    for i in list:        
        status=roster.getStatus(str(xmpp.protocol.JID(jid=i)))     
        name=roster.getName(str(xmpp.protocol.JID(jid=i)))
        #domyslne oznaczanie kontaktow jako niedostepnych
        if name==None: name=i
        widget.append([name,status,get_show('offline')[0],None,i,0])