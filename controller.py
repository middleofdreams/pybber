

import _importer,pynotify
from gtkmvc import Controller
from gtkmvc.adapters import Adapter
from chathelpers import *
from listhelpers import *
import os,sys,re,gobject,subprocess,threading

class MainCtrl (Controller):
	"""Handles signal processing, and keeps alignment of model and
	view"""
	def __init__(self, model, view):  
		Controller.__init__(self, model, view)  
		return  
		
		
	def register_view(self, view):
		# sets initial values for the view
		import statuslist
		statuslist.create(view)
		self.model.settings.loadprefs()
		if self.model.settings.remember=="True":
				view['checkbutton1'].set_active(True)
		self.model.connection.status=self.model.settings.status
		self.model.connection.show=self.model.settings.show
		view['list'].connect("row-activated", self.model.openchat)
		view['message'].get_buffer().connect_after("insert-text", self.msgbuffer)
		view['chat'].connect("key-release-event", self.chat_keypressed)
		view.icon.connect("activate", self.iconactivate) 
		view.icon.connect("popup_menu",self.iconmenu)
		view['chat'].connect("new-window-policy-decision-requested",self.link)
		pynotify.init("Pybber")
		return
		
	def link(self,widget,frame,request,navigation_action,policy):
		subprocess.Popen(["xdg-open",request.get_uri()])

		
	def chat_keypressed(self,widget, event):
		print gtk.gdk.keyval_name(event.keyval)
		if gtk.gdk.keyval_name(event.keyval) == 'x':
			widget.copy_clipboard()
		if gtk.gdk.keyval_name(event.keyval) == 'c':
			widget.copy_clipboard()
		if gtk.gdk.keyval_name(event.keyval) == 'v':
			self.view['message'].grab_focus()
			#self.view['message'].get_buffer().paste_clipboard()	
		

	def on_logonbtn_clicked(self,button):
		''' przy zalogowaniu '''
		jid=self.view['login'].get_text()
		pwd=self.view['passwd'].get_text()
		self.model.connection.connect_init(jid,pwd)
		remember=self.view['checkbutton1'].get_active()
		self.model.settings.saveacc(remember,jid,pwd)
		self.view['loginbox'].hide()	
	def register_adapters(self):
		ad = Adapter(self.model.settings, "login")
		ad.connect_widget(self.view["login"])
		ad = Adapter(self.model.settings, "pwd")
		ad.connect_widget(self.view["passwd"])
		 
	def iconmenu(self,widget, button, time, test = None):
		if button == 3:
			self.view['iconpopup'].show_all()
			self.view['iconpopup'].popup(None, None, None, 3, time)
	
	def property_newmessage_signal_emit(self, signal_name,args):
		'''odbior wiadomosci'''
		chat=striptext(args[3])
		chat=chat.replace("<","&lt;")
		chat=chat.replace(">","&gt;")
		chat=chat.replace("&lt;br/&gt;","<br/>")
		chat=chat.replace("&lt;br&gt;","<br/>")

		chat=intolink(chat)
		time,day=messtime(args[0])
		try:
			last=self.model.messagetype[args[1]]
		except:
			last="outgoing"
		self.model.messagetype[args[1]]="incoming"
		style=self.model.settings.style
		if args[2]==None: args[2]=args[1]
		if last=="incoming":
			continous=True
			text,archive=set_style(time,args[2],chat,False,True,style=style)
		else:
			continous=False
			text,archive=set_style(time,args[2],chat,False,style=style)
		text=showimages(text)
		#text=set_emoticons("grin",text)

		if args[1]==self.model.recipent:
			self.view.updatechat(unicode(text),continous=continous)
			
		else: 
			is_typing(self.view['listmodel'],args[1])
			
		try:
			self.model.messages[args[1]]+=archive
		except:
			html=self.model.archive.loadlast(args[1],self.model.settings.style,self.model.settings.me)
			self.model.messages[args[1]]=html+archive
		
		self.model.archive.archive_append(time,args[2],chat,day,args[1],text)
		#self.model.archive.archive_append(args[1],text,day)
		if not self.view['window'].is_active():
			gobject.idle_add(self.view['window'].set_urgency_hint,True)
			if self.model.settings.notify2=="True":
				self.view.iconblink()
			#text=intolink(text)
			#text=showimages(text)
		if not self.view['window'].is_active() or self.model.recipent!=args[1]:
			p = re.compile(r'<[^<]*?>')
			chat=p.sub('', chat)
			if self.model.settings.notify1=="True":
				self.view.notification(args[2],chat)
			if self.model.settings.notify2=="True":
				self.view.iconblink()
			
		
	def property_newpresence_signal_emit(self, signal_name,args):
		'''aktualizuje zmieniajace sie wpisy'''
		#guiclass.staticon.set_blinking(True)
		#sprawdzanie kto sie zmienil 
		jid=args[1].getFrom()
		nick=args[1].getFrom().getStripped()
		status=self.model.connection.roster.getStatus(jid.__str__())	
		priority= self.model.connection.roster.getPriority(jid.__str__())
	 
		#sprawdzenie czy zalogowany
		if priority==None:
			show='offline'
		else:	
			show=self.model.connection.roster.getShow(jid.__str__())		
		
		chitem=""
		import time
		while self.view['listmodel']==None:
			#time.sleep(1)
			pass
		item = self.view['listmodel'].get_iter_first ()
		while ( item != None ):
			if self.view['listmodel'].get_value (item, 4)==nick:
				chitem=item
			item = self.view['listmodel'].iter_next(item)
		#sprawdzenie czy kontakt znajduje sie na liscie	
		
		if chitem=="":
			show,priority=self.get_show(show)
			self.view.appendtolist([nick,status,show,None,nick,priority])
		else:
		#jesli tak - aktualizuj wpis
			nick=self.view['listmodel'].get_value(chitem,0)
			print "nick=%s \nstatus=%s"% (nick,status)
			if "\n" in nick:
				n=nick.split("\n")
				print n
				print n[0]
				if status!="" and status!=None:
					print "aaa"
					status=n[0]+"\n<i>"+status+"</i>"
				else: 
					status=n[0]
			else:
				if status!="" and status!=None:
					status=nick+"\n<i>"+status+"</i>"
				else: status=nick
				print "\n\nnewstatus=%s"%status
			print "final status="+status
			gobject.idle_add(self.view.updatelist,chitem,status,show)
			#time.sleep(1)
	
	def close(self,*args):
		import gtk,sys
		self.model.connection.cl=""
		self.model.connection=""
		gtk.main_quit()
		print "U don't like me anymore?... ;("
		sys.exit(0)
		
			# gtk signals
	def on_window_delete_event(self, window, event):
		window.hide()
		self.hidden=True
		return True
		
	def msgbuffer(self,text_buffer,position, text, lenght):
		'''wpisywanie tekstu'''
		start_iter, end_iter=text_buffer.get_bounds()
		self.model.editmessage[self.model.recipent]=text_buffer.get_text(start_iter,end_iter)

		if text == '\n' and position==text_buffer.get_start_iter:
			text_buffer.set_text('')
		if text =='\n':
			text_buffer.backspace(position,True, True)
		start_iter, end_iter=text_buffer.get_bounds()	
		if text_buffer.get_text(start_iter, end_iter)=="\n":
			text_buffer.set_text('')
	def on_button1_clicked(self,widget):
		self.sendmsg()		
			
	def on_message_key_press_event(self,widget, event):
		'''wysylanie wiadomosci
		TODO: SKROCIC JAKOS/PRZENIES GDZIES'''
		import gtk
		self.wfocus()
		if event.type == gtk.gdk.KEY_PRESS:
			buffer=self.view['message'].get_buffer()
			state= str(event.state)
			#print str(gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK)
			if gtk.gdk.keyval_name(event.keyval)== 'Return' :
				if "SHIFT" in state:
					self.view.message_newline()	
					#buffer.place_cursor(buffer.get_end_iter())
				else: self.sendmsg()
					
	def sendmsg(self):
		
		buffer=self.view['message'].get_buffer()
		start_iter=buffer.get_start_iter()
		end_iter=buffer.get_end_iter()
		self.model.editmessage[self.model.recipent]=""
		
		msg=buffer.get_text(start_iter, end_iter, include_hidden_chars=True)
		buffer.set_text("")
		

		# msg=str("ME:"+msg)
		if msg!="":
			ts=self.model.connection.send(msg,self.model.recipent)
			msg=msg.replace("<","&lt;")
			msg=msg.replace(">","&gt;")
			time,day=messtime(ts)
			msg=striptext(msg)
			msg=intolink(msg)
			msg=showimages(msg)

			try:
				last=self.model.messagetype[self.model.recipent]
			except:
				last="incoming"
			style=self.model.settings.style
			self.model.messagetype[self.model.recipent]="outgoing"
			if last=="outgoing":
				continous=True
				message,archive=set_style(time,self.model.settings.me,msg,continous=True,style=style)
			else:
				continous=False
				
				message,archive=set_style(time,self.model.settings.me,msg,style=style)
			try:
				self.model.messages[self.model.recipent]+=archive
			except:
				self.model.messages[self.model.recipent]=archive
			#guiclass.staticon.set_blinking(False)
			#time,day=messtime(ts)
			#savechat(guiclass,connection.vars,guiclass.recipent,"<font color=red>"+settings.me+"</font>",msg,time,day)
			#message=set_emoticons("grin",message)

			self.view.updatechat(message,continous=continous)
			self.model.archive.archive_append(time,self.model.settings.me,msg,day,self.model.recipent,message,out=True)

		#sendmsg(klasa,connection,settings)



	def show_hide(self, *widget):  #hide chat
		import gtk
		mainh=self.view['window'].get_size()[1]	
		self.model.recipent=""
		self.view.hide_chat(mainh)
		#self.vars.pos=self.view['window'].get_position()	
		# observable properties    
		
	def chat_clear(self, *widget):
		self.model.messagetype.pop(self.model.recipent)
		try:
			self.model.messages[self.model.recipent]=""
		except: pass
		template=self.model.settings.style_template()
		self.view.loadchat("",style=self.model.settings.style,template=template,variant=self.model.settings.stylevar)
		print self.view['message'].grab_focus()
		print "blalbabla"	
	def on_desc_key_press_event(self,widget,event):
		import gtk
		key=event.keyval
		if (key>31 and key<128) or (key==8 or key==65288):
			self.view.turn_desc_style(True)
		if  gtk.gdk.keyval_name(event.keyval)== 'Return':
			self.on_statusbar_changed()		
			
	def savesettings(self,widget):
		active = self.view['combobox2'].get_active()
		if active < 0:
		  show=0
		else:
			show=active
		status=self.view['entry8'].get_text()
		me=self.view['entry11'].get_text()
		if me=="":
			me=self.model.login
		style=self.view['chatstyle'].get_active()
		style=self.view['chatstyle'].get_model()[style][0]
		self.model.me=me
		if self.view['notify1'].get_active():notify1="True"
		else: notify1="False"
		if self.view['notify2'].get_active():notify2="True"
		else: notify2="False"
		if self.view['stylevarscheck'].get_active():
			index=self.view['stylevarslist'].get_active()
			model=self.view['stylevarslist'].get_model()
			variant=model[index][0]
		else:
			variant=""
		self.model.settings.save(show,status,me,style,variant,notify1,notify2)
		self.closesettings(widget)
		
	def closesettings(self,widget):
		mainh=self.view['window'].get_size()[1]	
		self.view.closesettings(mainh)

	def opensettings(self,widget):
		pathname = os.path.dirname(sys.argv[0])        
		path= os.path.abspath(pathname)
		styles=os.listdir(path+'/chatstyles/')
		try:
			stylevars=os.listdir(path+"/chatstyles/"+self.model.settings.style+"/Variants")
		except:
			stylevars=""	
		print stylevars
		self.view.opensettings(self.model.settings.get_all(),styles,stylevars)
		self.view['chatstyle'].connect("changed",self.check_style_variants)
		
	def check_style_variants(self,widget):
		self.view['stylevarsbox'].set_sensitive(0)
		self.view['stylevarscheck'].set_active(0)
		self.view['stylevarslist'].get_model().clear()
		model=widget.get_model()
		index=widget.get_active()
		style=model[index][0]
		path='chatstyles/'+style+'/Variants'
		if os.path.isdir(path):
			list=os.listdir(path)
			varlist=[]
			for i in list:
				if i.endswith(".css"):
					variant=i.rstrip(".css")
					varlist.append(variant)
			if len(varlist)>0:		
				self.view.create_style_variants(varlist)
	
			

	def on_statusbar_changed(self,*args):	
		desc=self.view['desc'].get_text()
		index=self.view['statusbar'].get_active()
		self.model.connection.set_status(index,desc)
		self.view.turn_desc_style(False)
	def on_list_button_press_event(self, treeview, event):
		if event.button == 3:
			x = int(event.x)
			y = int(event.y)
			time = event.time
			pthinfo = treeview.get_path_at_pos(x, y)
			if pthinfo is not None:
				path, col, cellx, celly = pthinfo
				treeview.grab_focus()
				treeview.set_cursor( path, col, 0)
				self.view['contactpopup'].popup( None, None, None, 3, time)
				return True

	def property_recipent_value_change(self, model, old, new):
		print model
		try:
			self.view['message'].get_buffer().set_text(self.model.editmessage[new])
		except:
			self.view['message'].get_buffer().set_text("")
		if old=="": 
			self.view.openchat()
			posx,posy=self.view['window'].get_position()
			posx=posx-400
			self.view['window'].move(posx,posy)
			sizex,sizey=self.view['window'].get_size()
			self.model.pos.set_pos(posx,posy)
		self.model.messagetype[new]=""
		try:
			html=model.messages[new]
		except:
			html=self.model.archive.loadlast(new,self.model.settings.style,self.model.settings.me)
			model.messages[new]=html
			print html
		template=self.model.settings.style_template()
		self.view.loadchat(html,style=self.model.settings.style,template=template,variant=self.model.settings.stylevar)
		if new==self.model.recipentname or self.model.recipentname==None :
			self.view['window'].set_title("Rozmowa z "+new)
		else:
			self.view['window'].set_title("Rozmowa z "+self.model.recipentname+" ("+new+")")
		self.view.archive_close()
		self.view.iconblink(False)
		gobject.idle_add(self.view['window'].set_urgency_hint,False)

		from listhelpers import show_back
		show_back(new,self.view['listmodel'])
		threading.Thread(target=self.align_chat,args=()).start()
		
	def iconactivate(self,widget):
		window=self.view['window']
		if not window.is_active():
			print self.model.hidden
			if self.model.hidden:
				newx,newy=self.model.pos.get_pos()
				print newx,newy
				window.move(newx,newy)
				self.model.hidden=False
			else:
				x,y=window.get_position()
				self.model.pos.set_pos(x,y)
			window.present()
			window.show()		
			self.view.icon.set_blinking(False)
			gobject.idle_add(self.view['window'].set_urgency_hint,False)

		if window.is_active():
			window.present()
			x,y=window.get_position()
			self.model.pos.set_pos(x,y)
			window.hide()
			self.model.hidden=True
	def wfocus(self,*args):
		self.view.iconblink(False)
		gobject.idle_add(self.view['window'].set_urgency_hint,False)

		pass
	def set_status_from_icon(self,widget):
		show=widget.name.lstrip("popupstatus")
		show=int(show)-1
		desc=self.view['desc'].get_text()
		self.model.connection.set_status(show,desc)
		self.view['statusbar'].set_active(show)
		
	def property_archiveclose_signal_emit(self, signalname,args):
		self.model.recipent=self.model.archive.open
		
	def zoomin(self,widget):
		self.view['chat'].zoom_in()
 
	def zoomout(self,widget):
		self.view['chat'].zoom_out()
	def property_composing_signal_emit(self,signalname,args):
		user,state=args
		if user==self.model.recipent:
			if state=="composing":
				self.view['state'].show()
				self.view['state'].set_text("pisze...")
			if state=="paused":
				self.view['state'].show()
				self.view['state'].set_text("przestal pisac")
			if state=="active":
				self.view['state'].hide()
				self.view['state'].set_text("")
	def property_archiveclose_signal_emit(self,signalname,args):
		self.property_recipent_value_change(self.model,None,args)
	def align_chat(self):
		import time
		time.sleep(0.5)
		self.view.align_chat()
		
