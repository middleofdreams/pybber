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

def is_typing(widget,jid):
	
	show=gtk.gdk.pixbuf_new_from_file("icons/typing.png")

	
	cats = list()
	item = widget.get_iter_first ()
	while ( item != None ):
		cats.append (widget.get_value (item, 4))
		item = widget.iter_next(item)
	#sprawdzenie czy kontakt znajduje sie na liscie	
	if not jid in cats:
		status=connection.roster.getStatus(jid)
		widget.append([jid,status,show,jid])
	else:
	#jesli tak - aktualizuj wpisj
		item = widget.get_iter_first ()
		
		while ( widget.get_value(item,4)!=jid):
			cats.append (widget.get_value (item, 4))
			item = widget.iter_next(item)
	pshow=widget.get_value(item,2)
	#tu gdzies trzeba sprawdzic czy juz ma zamieniona ikonke...
	#w najgorszym wypadku dodac kolejna kolumne gdzie bedzie tylko 
	#true/false gdy pisze lub nie
	#print widget.get_value(item,3)
	import gobject
	if widget.get_value(item,3)==None:
		gobject.idle_add(widget.set_value,item,3,pshow)
	gobject.idle_add(widget.set_value,item,2,show)

def show_back(recipent,model):

	if "@" in recipent:
		iter=model.get_iter_first()
		while model.get_value(iter,4)!=recipent or iter==None:
			iter=model.iter_next(iter)
		if iter!=None or iter!="":
			oldstatus=model.get_value(iter,3)
			if oldstatus!=None:
				model.set_value(iter,2,oldstatus)
				model.set_value(iter,3,None)
