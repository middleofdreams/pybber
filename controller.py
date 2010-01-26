

import _importer
from gtkmvc import Controller
from gtkmvc.adapters import Adapter
from chathelpers import *

class MyCtrl (Controller):
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
		return
		
		
	def register_adapters(self):
		ad = Adapter(self.model.settings, "login")
		ad.connect_widget(self.view["login"])
		ad = Adapter(self.model.settings, "pwd")
		ad.connect_widget(self.view["passwd"])

	
	def property_newmessage_signal_emit(self, signal_name,args):
		'''odbior wiadomosci'''
		chat=striptext(args[3])
		chat=intolink(chat)
		time,day=messtime(args[0])
		text="<i>("+time+")</i><b> <font color=blue>"+args[2]+"</font></b>: "+chat

		if args[1]==self.model.recipent:
			self.view.updatechat(unicode(text))
		try:
			self.model.messages[args[1]]+="<br/>"+text
		except:
			self.model.messages[args[1]]=text


			#text=intolink(text)
			#text=showimages(text)
			
		
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
		item = self.view['listmodel'].get_iter_first ()
		while ( item != None ):
			if self.view['listmodel'].get_value (item, 4)==nick:
				chitem=item
			item = self.view['listmodel'].iter_next(item)
		#sprawdzenie czy kontakt znajduje sie na liscie	
		if chitem=="":
			self.view.appendtolist([nick,status,self.get_show(show),None,nick])
		else:
		#jesli tak - aktualizuj wpis
			self.view.updatelist(chitem,status,show)
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
		self.close()
		return True
		
	def msgbuffer(self,text_buffer,position, text, lenght):
		'''wpisywanie tekstu'''
		if text == '\n' and position==text_buffer.get_start_iter:
			text_buffer.set_text('')
		if text =='\n':
			text_buffer.backspace(position,True, True)
		start_iter, end_iter=text_buffer.get_bounds()	
		if text_buffer.get_text(start_iter, end_iter)=="\n":
			text_buffer.set_text('')
			
	def on_message_key_press_event(self,widget, event):
		'''wysylanie wiadomosci
		TODO: SKROCIC JAKOS/PRZENIES GDZIES'''
		import gtk
		if event.type == gtk.gdk.KEY_PRESS:
			if gtk.gdk.keyval_name(event.keyval)== 'Return' :
				if event.state==gtk.gdk.SHIFT_MASK | gtk.gdk.MOD2_MASK or event.state==gtk.gdk.SHIFT_MASK:
					self.view.message_newline()
					#buffer.place_cursor(buffer.get_end_iter())
				else:
					buffer=self.view['message'].get_buffer()
					start_iter=buffer.get_start_iter()
					end_iter=buffer.get_end_iter()
					msg=buffer.get_text(start_iter, end_iter, include_hidden_chars=True)
					buffer.set_text("")
					msg=msg.replace("<","&lt;")
					msg=msg.replace(">","&gt;")

					# msg=str("ME:"+msg)
					if msg!="":
						ts=self.model.connection.send(msg,self.model.recipent)
						time,day=messtime(ts)
						msg=striptext(msg)
						msg=intolink(msg)
						message="<i>("+time+")</i><b> <font color=red>" \
							+self.model.settings.me+"</font></b>:"+msg
						try:
							self.model.messages[self.model.recipent]+="<br/>"+message
						except:
							self.model.messages[self.model.recipent]=message
						#guiclass.staticon.set_blinking(False)
						#time,day=messtime(ts)
						#savechat(guiclass,connection.vars,guiclass.recipent,"<font color=red>"+settings.me+"</font>",msg,time,day)
						self.view.updatechat(message)

					#sendmsg(klasa,connection,settings)

	def on_logonbtn_clicked(self,button):
		''' przy zalogowaniu '''
		jid=self.view['login'].get_text()
		pwd=self.view['passwd'].get_text()
		self.model.connection.connect_init(jid,pwd)
		#self.settings.saveacc(self)
		self.view['loginbox'].hide()
		#self.view['jidlabel'].set_label(jid)	
		
		#self.staticon.set_from_file("icons/disconnected.png") 
		return

	def show_hide(self, *widget):  #hide chat
		import gtk
		mainh=self.view['window'].get_size()[1]	
		self.model.recipent=""
		self.view.hide_chat(mainh)
		#self.vars.pos=self.view['window'].get_position()	
		# observable properties    
		
	def chat_clear(self, *widget):
		try:
			self.model.messages[self.model.recipent]=""
		except: pass
		self.view.loadchat("")
			
	def on_desc_key_press_event(self,widget,event):
		import gtk
		self.view.turn_desc_style(True)
		if  gtk.gdk.keyval_name(event.keyval)== 'Return':
			self.on_statusbar_changed()		
	def on_statusbar_changed(self,*args):	
		desc=self.view['desc'].get_text()
		index=self.view['statusbar'].get_active()
		self.model.connection.set_status(index,desc)
		self.view.turn_desc_style(False)
	def changedata(self, *widget):
		self.view.changedata()

	def hidewarn(self,widget):
		self.view.hidewarn()
	def reconnect(self,widget):
		self.model.connection.reconnect()
		self.view.reconnect()
	def reconnect2(self,widget):
		self.connection.reconnect2()
	def property_recipent_value_change(self, model, old, new):
		if old=="": self.view.openchat()
		try:
			html=model.messages[new]
		except:
			html=""
		self.view.loadchat(html)
		pass # end of class
