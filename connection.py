# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,threading,time,gobject,sys,thread,pynotify
from chatwindow import *
from list import *
#----------klasa do zarzadzania polaczeniem-------------------------#

class connection(threading.Thread):
	def __init__(self,guiclass):
		
		#przypisanie paru zmiennych z glownej klasy
		self.gui=guiclass
		self.desc=guiclass.desc
		self.chat=guiclass.chat
		self.statusbar=guiclass.statusbar
		self.progress=guiclass.progress
		self.statusentry=guiclass.statusentry
		self.toolong=guiclass.toolong
		self.not_connected=guiclass.not_connected
		
	
        #pare zmiennych
		self.i=0.00 #licznik czasu polaczenie
		self.active=False #okresla czy jest nawiazane aktywne polaczenie
		self.stop=False #okresla czy polaczenie jest 'przerywane'
	def connect_init(self,guiclass,jid,pwd):
		self.jid=jid
		self.pwd=pwd
		#rozpoczecie watku polaczenia
	#	print jid
	#	print pwd
		threading.Thread.__init__(self)
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
			self.gui.loginbox.hide()
			self.cl=cl
			#wylaczenie progressbara
			self.ifrun=False
			self.active=True
			self.statusentry.show()
			self.statusbar.show()
			self.statusentry.set_sensitive(1)
			self.statusbar.set_sensitive(1)
			#handler do odbierania wiadomosci
			
		
			
			#ustawienie poczatkowego statusu
			self.cl.sendInitPresence()
			self.cl.send(xmpp.dispatcher.Presence(priority=5, show=None,status=""))
			self.desc.set_text(self.gui.settings.status)
			self.statusbar.set_active(0)
			self.get_list()
			#chowa ewentualne komunikaty
			self.toolong.hide()
			self.not_connected.hide()
			
			
			self.cl.UnregisterDisconnectHandler(self.cl.DisconnectHandler)
			self.cl.RegisterDisconnectHandler(self.disconnected)

			self.set_status(self.gui.settings.show,self.gui.settings.status)
			self.gui.statusbar.set_active(self.gui.settings.show)
			time.sleep(0.2)
			self.cl.RegisterHandler('presence',self.presenceCB)
			self.cl.RegisterHandler('message',self.messageCB)
			####wykrywanie rozlaczenia
			self.disconnecttry=0
			threading.Thread(target=self.is_connected,args=()).start()	
			threading.Thread(target=self.is_connected,args=()).start()	
			#########################################################
			
			
			#to rowniez do odbierania wiadomosci
			self.GoOn(self.cl)

		
#---------Pasek postepu i sprawdzenie czasu polaczenia------------------		
	def connectbar(self):
		
		#reset zmiennej stop
		self.stop=False
		
		gobject.idle_add(self.progress.show)

		self.i=0.00
		#Dopoki nie polaczany i self.i mniejsze od 1 dodawaj do paska		
		while(self.ifrun and self.i<1):
			gobject.idle_add(self.progress.set_fraction,self.i)

			time.sleep(0.1)
			self.i=self.i+0.005
			
			#wyswietlanie komunikatu o za dlugim polaczeniu:
			if(str(self.i)=='0.15'):
				self.toolong.show()
				
			#przerwanie petli po nacisnieciu przycisku z komunikatu
			if self.stop:
				break
		
		#ukrycie progressbara
		gobject.idle_add(self.progress.hide)
		
		#jesli polaczony w czasie krotszym niz 25s
		if(not self.ifrun and self.i<1 and not self.stop):
			#ustaw zmienna odpowiadajaca za aktywne polaczenie
			self.active=True
			self.gui.staticon.set_from_file("icons/pybber.png") 
			
		#jesli polaczenie bylo 'przerwane'
		if self.stop:
			#zrestartuj polaczenie
			threading.Thread(target=self.connecting,args=()).start()	

		#jesli minelo 25 i sie nie polaczyl i nie bylo reakcji usera
		if(str(self.i)=='1.0'):
			#wyswietl komunikat o bledzie
				self.toolong.hide()
				if not self.active:
					self.not_connected.show()
		
#----------funkcje dla komunikatow--------------------------------------
	def reconnect(self):
		self.stop=True
		self.toolong.hide()
	def reconnect2(self):
		self.not_connected.hide()
		threading.Thread(target=self.connecting,args=()).start()	


#------funkcje do komunikacji z serwerem--------------------------------

	def send(self,msg):
		'''wysyla wiadomosc'''
		mess=xmpp.Message(self.gui.recipent,msg,typ='chat')
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
		
		# pobieranie WSZYSTKICH kontaktow z rostera	
		get_all(self.gui,items)
		
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
			time,day=messtime(ts)
			user=user.getStripped()
			name=self.roster.getName(user)
			if name=="": name=user
			savechat(self.gui,user,name,text,time,day)
			#wypisywanie tresci w oknie
			if user==self.gui.recipent:
				gobject.idle_add(loadchat,self.gui,user)
			else:
				is_typing(self.gui,user)
				
			if not self.gui.window.is_active():
				self.gui.window.set_urgency_hint(True)
				self.gui.staticon.set_blinking(True)
				self.gui.notification(user,text)
			else:
				self.gui.staticon.set_blinking(False)
				self.gui.window.set_urgency_hint(False)

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
		update_list(self.gui,sess,pres)
		
	def disconnected(self):
		self.gui.listmodel.clear()
		self.active=False
		self.connect_init(self.gui,self.gui.settings.login,self.gui.settings.pwd)


	def is_connected(self):
		while self.active:
			time.sleep(5)
			 #self.cl.Roster.getRawRoster()
			if self.cl.Roster.getRoster() == "":
				self.disconnecttry=self.disconnecttry+1
			else: 
				if self.disconnecttry>0: self.disconnecttry=self.disconnecttry-1
			if self.disconnecttry>3: self.disconnected()
