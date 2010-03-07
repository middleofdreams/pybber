import gtk
import gobject,re
def get_show(show):
	'''pobiera obrazek statusu'''
	import gtk
	priority=0
	if show==None:
		show=gtk.gdk.pixbuf_new_from_file("icons/online.png")
		priority=5
	if show=="dnd":
		show=gtk.gdk.pixbuf_new_from_file("icons/busy.png")
		priority=2
	if show=="chat":
		show=gtk.gdk.pixbuf_new_from_file("icons/chat.png")	
		priority=6
	if show=="away":
		show=gtk.gdk.pixbuf_new_from_file("icons/away.png")
		priority=4
	if show=="xa":
		show=gtk.gdk.pixbuf_new_from_file("icons/extended-away.png")
		priority=3
	if show=='offline':
		show=gtk.gdk.pixbuf_new_from_file("icons/offline.png")
	if show=='unavailable':
		show=gtk.gdk.pixbuf_new_from_file("icons/offline.png")
	return show,priority
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
	
	if widget.get_value(item,3)==None:
		gobject.idle_add(widget.set_value,item,3,pshow)
		widget.set_value(item,5,widget.get_value(item,5)+20)
		nick=widget.get_value(item,0)
		nick=make_bold(nick)
		gobject.idle_add(widget.set_value,item,0,nick)
		
	gobject.idle_add(widget.set_value,item,2,show)
	
def make_bold(nick,bold=True):
	statch=False
	if "\n" in nick:
		n=nick.split("\n",1)
		nick=n[0]
		status=n[1]
		statch=True
	p = re.compile(r'<[^<]*?>')
	nick=p.sub('', nick)
	if bold:
		nick="<b>"+nick+"</b>"
	if statch:
		nick=nick+"\n"+status
	return nick
			
def show_back(recipent,model):

	if "@" in recipent:
		iter=model.get_iter_first()
		while model.get_value(iter,4)!=recipent or iter==None:
			iter=model.iter_next(iter)
		if iter!=None or iter!="":
			nick=model.get_value(iter,0)
			nick=make_bold(nick,bold=False)
			gobject.idle_add(model.set_value,iter,0,nick)
			oldstatus=model.get_value(iter,3)
			if oldstatus!=None:
				model.set_value(iter,2,oldstatus)
				model.set_value(iter,3,None)
				model.set_value(iter,5,model.get_value(iter,5)-20)
