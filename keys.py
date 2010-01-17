import gtk
from chatwindow import copyfromchat
def message(widget, event, klasa):
	if event.type == gtk.gdk.KEY_PRESS:
		if gtk.gdk.keyval_name(event.keyval)== 'Return' :
			if event.state==gtk.gdk.SHIFT_MASK:
				buffer=klasa.message.get_buffer()
				buffer.insert(buffer.get_end_iter(),chr(13))
				buffer.place_cursor(buffer.get_end_iter())
			else:
				klasa.send()
	
def status(widget, event, klasa):
	if event.type == gtk.gdk.KEY_PRESS:
		if gtk.gdk.keyval_name(event.keyval)== 'Return' :
			klasa.chdesc()

def list(widget, event, klasa):
	if event.type == gtk.gdk.KEY_PRESS:
		if gtk.gdk.keyval_name(event.keyval)== 'Delete' :
			klasa.deluser(klasa)

def chat(widget, event, klasa):
	if gtk.gdk.keyval_name(event.keyval) == 'x':
		copyfromchat(klasa)
	if gtk.gdk.keyval_name(event.keyval) == 'c':
		copyfromchat(klasa)
	if gtk.gdk.keyval_name(event.keyval) == 'v':
		klasa.message.grab_focus()
		klasa.message.paste_clipboard()	
