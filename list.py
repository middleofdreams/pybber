import gtk,xmpp
from listhelpers import *
print "Aaaa"
def create_empty_list(view):
    '''tworzy pusta liste'''
    view['listmodel']=gtk.ListStore(str,str,gtk.gdk.Pixbuf,gtk.gdk.Pixbuf,str)
    view['list'].set_model(view['listmodel'])
    lrenderer=gtk.CellRendererText()
    lcolumn=gtk.TreeViewColumn("Kontakty:",lrenderer, text=0)
    lcolumn2=gtk.TreeViewColumn("Opisy",lrenderer, text=1)
    lcolumn3=gtk.TreeViewColumn("Statusy",gtk.CellRendererPixbuf(), pixbuf=2)
    view['list'].append_column(lcolumn3)
    view['list'].append_column(lcolumn)
    view['list'].append_column(lcolumn2)
    view['list'].set_headers_visible(0)
    
def get_all(list,widget,roster):    
    '''pobiera wszystkie kontakty z rostera'''
    for i in list:        
        status=roster.getStatus(str(xmpp.protocol.JID(jid=i)))     
        name=roster.getName(str(xmpp.protocol.JID(jid=i)))
        #domyslne oznaczanie kontaktow jako niedostepnych
        if name==None: name=i
        widget.append([name,status,get_show('offline'),None,i])