import gtk
from chatwindow import copyfromchat
def message(widget, event, klasa):
	if event.type == gtk.gdk.KEY_PRESS:
		if gtk.gdk.keyval_name(event.keyval)== 'Return' :
			if event.state==gtk.gdk.SHIFT_MASK:
				buffer=klasa.message.get_buffer()
				buffer.insert_at_cursor(chr(13))
				#buffer.place_cursor(buffer.get_end_iter())
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
		
def msgbuffer(text_buffer, position, text, lenght):
	if text == '\n' and position==text_buffer.get_start_iter:
		text_buffer.set_text('')
	if text =='\n':
		text_buffer.backspace(position,True, True)
	start_iter, end_iter=text_buffer.get_bounds()	
	if text_buffer.get_text(start_iter, end_iter)=="\n":
		text_buffer.set_text('')
