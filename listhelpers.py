import gtk
def get_show(show):
	'''pobiera obrazek statusu'''
	import gtk
	if show==None:
		show=gtk.gdk.pixbuf_new_from_file("icons/online.png")
	if show=="dnd":
		show=gtk.gdk.pixbuf_new_from_file("icons/busy.png")
	if show=="chat":
		show=gtk.gdk.pixbuf_new_from_file("icons/chat.png")	
	if show=="away":
		show=gtk.gdk.pixbuf_new_from_file("icons/away.png")
	if show=="xa":
		show=gtk.gdk.pixbuf_new_from_file("icons/extended-away.png")
	if show=='offline':
		show=gtk.gdk.pixbuf_new_from_file("icons/offline.png")
	if show=='unavailable':
		show=gtk.gdk.pixbuf_new_from_file("icons/offline.png")
	return show
pass 
