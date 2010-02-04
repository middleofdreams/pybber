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

    view['listmodel'].set_sort_func(5,compare_data)
    view['listmodel'].set_sort_column_id(5,gtk.SORT_DESCENDING)



def get_all(list,widget,roster):    
    '''pobiera wszystkie kontakty z rostera'''
    for i in list:        
        status=roster.getStatus(str(xmpp.protocol.JID(jid=i)))     
        name=roster.getName(str(xmpp.protocol.JID(jid=i)))
        #domyslne oznaczanie kontaktow jako niedostepnych
        if name==None: name=i
        widget.append([name,status,get_show('offline')[0],None,i,0])

def compare_data(model, iter1, iter2):
    data1 = model.get_value(iter1,5)
    data2 = model.get_value(iter2,5)
    if data1==data2:
        #if same vals:
        data1 = model.get_value(iter2,0)
        data2 = model.get_value(iter1,0)
        #sort by other column in reverse order
        data2=data2.lower()
        data1=data1.lower()
        #just for make it case insensitive
        #no need adding it for column 5 - there are integers
    return cmp(data1, data2)