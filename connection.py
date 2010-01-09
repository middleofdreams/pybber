# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,threading,time,xmpp,gobject,sys


#----------klasa do zarzadzania polaczeniem-------------------------#

class connection(threading.Thread):
	def __init__(self,guiclass):

		#przypisanie paru zmiennych z glownej klasy

		self.desc=guiclass.desc
		self.chat=guiclass.chat
		self.statusbar=guiclass.statusbar
		self.progress=guiclass.progress
		
        #rozpoczecie watku polaczenia
	
		threading.Thread.__init__(self)
		threading.Thread(target=self.connecting,args=()).start()
		
#-------lączenie z serwerem-----------------------------------------#
		
	def connecting(self):
		self.ifrun=True
		#start watku z progressbarem
		
		threading.Thread(target=self.connectbar,args=()).start()
		
		#todo - dane do polaczenia pobrac z kreatora       !!!
		
		jid = 'pybberclient@gmail.com' 
		pwd   = 'pybberjabber'
		jid=xmpp.protocol.JID(jid)  
		self.cl=xmpp.Client(jid.getDomain(),debug=[])
		if self.cl.connect() == "":
			print "not connected"
			sys.exit(0) 
		if self.cl.auth(jid.getNode(),pwd) == None: 
			print "authentication failed"
			sys.exit(0)
			
		#handler do odbierania wiadomosci
		
		self.cl.RegisterHandler('message',self.messageCB)
		
		#wylaczenie progressbara
		self.ifrun=False
		
		#ustawienie poczatkowego statusu
		self.cl.sendInitPresence()
		self.cl.send(xmpp.dispatcher.Presence(priority=5, show=None,status="Pybber test"))
		self.desc.set_text("Pybber test")
		self.statusbar.set_active(0)
		
		#to rowniez do odbierania wiadomosci
		self.GoOn(self.cl)
		
	def connectbar(self):
		gobject.idle_add(self.progress.show)
		while(self.ifrun):
			time.sleep(0.1)
			gobject.idle_add(self.progress.pulse)
		gobject.idle_add(self.progress.hide)
	def send(self,msg):
		self.cl.send(xmpp.Message("edpl90@gmail.com",msg))
		
	def set_desc(self,desc):
		self.cl.send(xmpp.dispatcher.Presence(priority=5, show=None,status=desc))
	def set_status(self,index,desc):
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
		

#------------Odbieranie wiadomosci:-------------------------------------

	def messageCB(self,conn,mess):
		text=mess.getBody()
		user=mess.getFrom()
		
		#pobranie usera i tresci nadchodzacej rozmowy
		
		if text!=None:
			user=user.getStripped()
			
			#wypisywanie tresci w oknie
			
			self.chat.append([user+": "+text])


	#funkcje sledzace wiadomosci:
	def StepOn(self, conn):
		try:
			conn.Process(1)
		except KeyboardInterrupt: return 0
		return 1

	def GoOn(self,conn):
		while self.StepOn(conn): pass
