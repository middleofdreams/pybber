# -*- coding: utf-8 -*-
#!/usr/bin/env python

import _importer
from gtkmvc import ModelMT,observable

import pygtk,gtk,xmpp,threading,time,gobject,sys,thread,pynotify
class ConnectionModel (ModelMT):
	stop=False
	active=False
	connecting=True
	i=0.00
	jid=""
	newmessage=observable.Signal()
	newpresence=observable.Signal()
	__observables__ = ('stop','active','connecting','i','jid', \
	'newmessage', 'newpresence')
	
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
		#rozpoczecie watku polaczenia
	#	print jid
	#	print pwd
		threading.Thread(target=self.connecting,args=()).start()
		
#-------lączenie z serwerem-----------------------------------------#
		
	def connecting(self):
		self.ifrun=True
		#start watku z progressbarem
		
		threading.Thread(target=self.connectbar,args=()).start()
		
		jid=xmpp.protocol.JID(self.jid) 
		
		# testowe polaczenie:
		cl=xmpp.Client(jid.getDomain(),debug=[])
		if cl.connect() == "":
			print "not connected"
			sys.exit(0) 
		if not self.active:
			if cl.auth(jid.getNode(),self.pwd) == None: 
				print "authentication failed"
				sys.exit(0)
		
		#jesli polaczy sie w czasie krotszym niz pare sekund przyjmij
		#jako glowne polaczenie:
		if not self.active:	
			#self.gui.loginbox.hide()
			self.cl=cl
			self.cl.sendInitPresence()
			self.cl.send(xmpp.dispatcher.Presence(priority=5, show=None,status=""))
			#wylaczenie progressbara
			self.ifrun=False
			self.active=True
			#self.gui.desc.show()
			#self.gui.statusbar.show()
			#self.gui.desc.set_sensitive(1)
			#self.gui.statusbar.set_sensitive(1)
			#handler do odbierania wiadomosci
			
		
			
			#ustawienie poczatkowego statusu
			
			
			
			
			#self.cl.UnregisterDisconnectHandler(self.cl.DisconnectHandler)
			#self.cl.RegisterDisconnectHandler(self.disconnected)

			self.set_status(self.show,self.status)
			time.sleep(0.2)
			self.cl.RegisterHandler('message',self.messageCB)

			####wykrywanie rozlaczenia
			self.disconnecttry=0
			#threading.Thread(target=self.is_connected,args=()).start()	
			#threading.Thread(target=self.is_connected,args=()).start()	
			#########################################################
			
			
			#to rowniez do odbierania wiadomosci
			time.sleep(1)
			self.GoOn(self.cl)

		
#---------Pasek postepu i sprawdzenie czasu polaczenia------------------		
	def connectbar(self):
		
		#reset zmiennej stop
		self.stop=False
		self.i=0.00
		self.connecting=True

		
		#Dopoki nie polaczany i self.i mniejsze od 1 dodawaj do paska		
		while(self.ifrun and self.i<1.000):

			time.sleep(0.1)
			self.i=self.i+0.005
			
			#wyswietlanie komunikatu o za dlugim polaczeniu:
			
				
			#przerwanie petli po nacisnieciu przycisku z komunikatu
			if self.stop:
				break
		
		#ukrycie progressbara
		self.connecting=False
		
		#jesli polaczony w czasie krotszym niz 25s
		if(not self.ifrun and self.i<1 and not self.stop):
			#ustaw zmienna odpowiadajaca za aktywne polaczenie
			self.active=True
			
			
		#jesli polaczenie bylo 'przerwane'
		if self.stop:
			#zrestartuj polaczenie
			threading.Thread(target=self.connecting,args=()).start()	

		
#----------funkcje dla komunikatow--------------------------------------
	def reconnect(self):
		self.stop=True
		threading.Thread(target=self.connecting,args=()).start()	

		



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
		if index==1:
			self.cl.send(xmpp.dispatcher.Presence(show="away",status=desc))
		if index==2:
			self.cl.send(xmpp.dispatcher.Presence(show="xa",status=desc))
		if index==3:
			self.cl.send(xmpp.dispatcher.Presence(show="dnd",status=desc))
		if index==4:
			self.cl.send(xmpp.dispatcher.Presence(show="chat",status=desc))
		if index==5:
			self.cl.send(xmpp.dispatcher.Presence(show="unavailable",status=desc))
		
	def get_list(self):
		'''pobiera liste kontaktow'''
		self.roster=self.cl.Roster.getRoster()
		items=self.roster.getItems()
		self.cl.RegisterHandler('presence',self.presenceCB)

		# pobieranie WSZYSTKICH kontaktow z rostera	
		return items
		
#------------Odbieranie wiadomosci:-------------------------------------

	def messageCB(self,conn,mess):
		text=mess.getBody()
		user=mess.getFrom()
		
		#pobranie usera i tresci nadchodzacej rozmowy
		ts=mess.getTimestamp()
		if ts==None:
			ts=mess.setTimestamp()
			ts=mess.getTimestamp()
		
		if text!=None:
			#time,day=messtime(ts)
			user=user.getStripped()
			name=self.roster.getName(user)
			if name=="": name=user
			self.newmessage.emit([ts,user,name,text])
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

