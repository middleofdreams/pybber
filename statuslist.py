# -*- coding: utf-8 -*-
#!/usr/bin/env python
import gtk
def create(view):	
	view['statuslist']=gtk.ListStore(str,gtk.gdk.Pixbuf)
	view['statusbar'].set_model(view['statuslist'])
	view['statuslist'].append(["Dostępny",gtk.gdk.pixbuf_new_from_file("icons/online.png")])
	view['statuslist'].append(["Zaraz wracam",gtk.gdk.pixbuf_new_from_file("icons/away.png")])
	view['statuslist'].append(["Wrócę później",gtk.gdk.pixbuf_new_from_file("icons/extended-away.png")])
	view['statuslist'].append(["Nie przeszkadzać",gtk.gdk.pixbuf_new_from_file("icons/busy.png")])
	view['statuslist'].append(["Chcę pogadać",gtk.gdk.pixbuf_new_from_file("icons/chat.png")])
	view['statuslist'].append(["Niewidoczny",gtk.gdk.pixbuf_new_from_file("icons/invisible.png")])
	cell = gtk.CellRendererText()
	cell2=gtk.CellRendererPixbuf()
	cell2.set_fixed_size(24,24)
	view['statusbar'].pack_start(cell2,expand=False)
	view['statusbar'].pack_start(cell)
	view['statusbar'].add_attribute(cell2, 'pixbuf', 1)
	view['statusbar'].add_attribute(cell, 'text', 0)
