# -*- coding: utf-8 -*-
#!/usr/bin/env python

import _importer
from gtkmvc import ModelMT,observable

import pygtk,gtk,xmpp,threading,time,gobject,sys,thread,pynotify
class ConnectionModel (ModelMT):
	stop=False
	active=False
	is_connecting=None
	i=0.00
	jid=""
	tryid=0
	autherror=False
	connerror=0
	newmessage=observable.Signal()
	newpresence=observable.Signal()
	composing=observable.Signal()
	__observables__ = ('stop','active','is_connecting','i','jid', \
	'newmessage', 'newpresence','composing','connerror','autherror')
	
	def __init__(self):
		ModelMT.__init__(self)
		#przypisanie paru zmiennych z glownej klasy
		#self.gui=guiclass
		#self.vars=vars
		#self.settings=settings
	
        #pare zmiennych
		self.i=0.00 #licznik czasu polaczenie
		#self.active=False #okresla czy jest nawiazane aktywne polaczenie
		#self.stop=False #okresla czy polaczenie jest 'przerywane'
	def connect_init(self,jid,pwd):
		self.jid=jid
		self.pwd=pwd
		self.is_connecting=True
		#rozpoczecie watku polaczenia
	#	print jid
	#	print pwd
		self.th=threading.Thread(target=self.connecting,args=())
		self.th.start()
		
#-------lączenie z serwerem-----------------------------------------#
		
	def connecting(self):
		self.ifrun=True
		self.autherror=False
		#start watku z progressbarem
		self.tryid+=1

		threading.Thread(target=self.connectbar,args=()).start()
		
		jid=xmpp.protocol.JID(self.jid) 
		# testowe polaczenie:
		cl=xmpp.Client(jid.getDomain(),debug=[])
		if cl.connect() == "":
			print "not connected"
			self.connerror+=1
			sys.exit(0) 
		if not self.active:
			if cl.auth(jid.getNode(),self.pwd) == None: 
				print "authentication failed"
				self.autherror=True
				sys.exit(0)
		
		#jesli polaczy sie w czasie krotszym niz pare sekund przyjmij
		#jako glowne polaczenie:
		if not self.active:	
			#self.gui.loginbox.hide()
			self.cl=cl
			self.cl.sendInitPresence()
			self.cl.send(xmpp.dispatcher.Presence(priority=5, show="unavailable",status=""))
			#wylaczenie progressbara
			self.ifrun=False
			self.active=True
			#self.gui.desc.show()
			#self.gui.statusbar.show()
			#self.gui.desc.set_sensitive(1)
			#self.gui.statusbar.set_sensitive(1)
			#handler do odbierania wiadomosci
			
		
			
			#ustawienie poczatkowego statusu
			
			
			
			
			self.cl.UnregisterDisconnectHandler(self.cl.DisconnectHandler)
			self.cl.RegisterDisconnectHandler(self.disconnected)

			
			time.sleep(0.2)
			self.cl.RegisterHandler('message',self.messageCB)
			self.cl.RegisterHandler('',self.test)
			####wykrywanie rozlaczenia
			self.disconnecttry=0
			#threading.Thread(target=self.is_connected,args=()).start()	
			#threading.Thread(target=self.is_connected,args=()).start()	
			#########################################################
			
			
			#to rowniez do odbierania wiadomosci
			time.sleep(1)
			self.set_status(self.show,self.status)
			self.GoOn(self.cl)

		
#---------Pasek postepu i sprawdzenie czasu polaczenia------------------		
	def connectbar(self):
		
		#reset zmiennej stop
		self.stop=False
		self.i=0.00
		self.is_connecting=True

		
		#Dopoki nie polaczany i self.i mniejsze od 1 dodawaj do paska		
		while(self.ifrun and self.i<1.000):

			if self.stop:
				#threading.Thread(target=self.connecting,args=()).start()
				break
			time.sleep(0.1)
			self.i=self.i+0.005
			
			#wyswietlanie komunikatu o za dlugim polaczeniu:
			
				
			#przerwanie petli po nacisnieciu przycisku z komunikatu
			if self.stop:
				#threading.Thread(target=self.connecting,args=()).start()
				break
			    
		#ukrycie progressbara
		
		self.is_connecting=False
		#jesli polaczony w czasie krotszym niz 25s
		if(not self.ifrun and self.i<1 and not self.stop):
			#ustaw zmienna odpowiadajaca za aktywne polaczenie
			self.active=True
			
			
		#jesli polaczenie bylo 'przerwane'
		
		
#----------funkcje dla komunikatow--------------------------------------
	def reconnect(self):
		self.stop=True
		time.sleep(0.2)

		#self.th.exit()
		self.i=0.00
		#del self.th
		try:
			self.connect_init(self.jid, self.pwd)

		except: pass



#------funkcje do komunikacji z serwerem--------------------------------

	def send(self,msg,recipent):
		'''wysyla wiadomosc'''
		mess=xmpp.Message(recipent,msg,typ='chat')
		mess.setTimestamp()
		self.cl.send(mess)
		return mess.getTimestamp()
		
	def set_desc(self,desc):
		'''ustawia opis'''
		self.cl.send(xmpp.dispatcher.Presence(priority=5, show=None,status=desc))
		
	def set_status(self,index,desc):
		'''ustawia status'''
		if index=="": index=0
		if index==0:
			self.cl.send(xmpp.dispatcher.Presence(show=None,status=desc))
			return None
		if index==1:
			self.cl.send(xmpp.dispatcher.Presence(show="away",status=desc))
			return "away"
		if index==2:
			self.cl.send(xmpp.dispatcher.Presence(show="xa",status=desc))
			return "xa"
		if index==3:
			self.cl.send(xmpp.dispatcher.Presence(show="dnd",status=desc))
			return "dnd"
		if index==4:
			self.cl.send(xmpp.dispatcher.Presence(show="chat",status=desc))
			return "chat"
		if index==5:
			self.cl.send(xmpp.dispatcher.Presence(show="unavailable",status=desc))
			return "unavailable"
		
	def get_list(self):
		'''pobiera liste kontaktow'''
		self.roster=self.cl.Roster.getRoster()
		items=self.roster.getItems()
		self.cl.RegisterHandler('presence',self.presenceCB)

		# pobieranie WSZYSTKICH kontaktow z rostera	
		return items
		
#------------Odbieranie wiadomosci:-------------------------------------
	def test(self,conn,iq):
		print conn
		print iq
	def messageCB(self,conn,mess):
		list=mess.getChildren()
		text=mess.getBody()
		user=mess.getFrom()
		composing=False
		paused=False
		active=False
		for i in list:
			state=i.getName()
			if state=="composing":
				composing=True
			if state=="paused":
				paused=True
			if state=="active":
				active=True
			
		
		#pobranie usera i tresci nadchodzacej rozmowy
		ts=mess.getTimestamp()
		if ts==None:
			ts=mess.setTimestamp()
			ts=mess.getTimestamp()
		
		user=user.getStripped()
		name=self.roster.getName(user)
		if name=="": name=user
		if text!=None:
			#time,day=messtime(ts)

			self.newmessage.emit([ts,user,name,text])
		if composing:
			self.composing.emit([user,"composing"])
		if paused:
			self.composing.emit([user,"paused"])
		if active:
			self.composing.emit([user,"active"])
			#savechat(self.gui,self.vars,user,name,text,time,day)
			#wypisywanie tresci w oknie
			#if user==self.gui.recipent and user!=self.vars.archiveopen:
				#gobject.idle_add(loadchat,self.gui,user)
			#	gobject.idle_add(updatechat,self.gui,user,name,text,time)
			#else:
			#	gobject.idle_add(is_typing,self.gui,user)
			#if not self.gui.window.is_active():
				#self.gui.window.set_urgency_hint(True)
			#	gobject.idle_add(self.gui.staticon.set_blinking,True)
			#	gobject.idle_add(self.gui.notification,user,text)
			#else:
			#	self.gui.staticon.set_blinking(False)
			#	self.gui.window.set_urgency_hint(False)

	#funkcje sledzace wiadomosci:
	def StepOn(self, conn):
		try:
			conn.Process(1)
			
		except KeyboardInterrupt: 
			return 0
		return 1
		

	def GoOn(self,conn):
		while self.StepOn(conn): pass
		#print "aa"
	#funkcja sledzaca aktywnosc userow	
	def presenceCB(self, sess,pres):
		#print sess,pres
		self.newpresence.emit([sess,pres])
		#update_list(self.gui,sess,pres,self)
		pass
		
	def disconnected(self):
		self.gui.listmodel.clear()
		self.active=False
		self.connect_init(self.gui,self.settings.login,self.settings.pwd)


	def is_connected(self):
		while self.active:
			time.sleep(5)
			 #self.cl.Roster.getRawRoster()
			if self.cl.Roster.getRoster() == "":
				self.disconnecttry=self.disconnecttry+1
			else: 
				if self.disconnecttry>0: self.disconnecttry=self.disconnecttry-1
			if self.disconnecttry>3: self.disconnected()

