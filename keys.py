import gtk

def message(widget, event, klasa):
	if event.type == gtk.gdk.KEY_PRESS:
		if gtk.gdk.keyval_name(event.keyval)== 'Return' :
			klasa.send()
	
def status(widget, event, klasa):
	if event.type == gtk.gdk.KEY_PRESS:
		if gtk.gdk.keyval_name(event.keyval)== 'Return' :
			klasa.chdesc()

def list(widget, event, klasa):
	if event.type == gtk.gdk.KEY_PRESS:
		if gtk.gdk.keyval_name(event.keyval)== 'Delete' :
			klasa.deluser(klasa)
