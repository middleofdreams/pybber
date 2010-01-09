# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,threading,time,xmpp,gobject,sys,thread


#----------klasa do zarzadzania polaczeniem-------------------------#

class connection(threading.Thread):
	def __init__(self,guiclass):

		#przypisanie paru zmiennych z glownej klasy
	
		self.desc=guiclass.desc
		self.chat=guiclass.chat
		self.statusbar=guiclass.statusbar
		self.progress=guiclass.progress
		self.toolong=guiclass.toolong
		self.not_connected=guiclass.not_connected
		
        #pare zmiennych
		self.i=0.00 #licznik czasu polaczenie
		self.active=False #okresla czy jest nawiazane aktywne polaczenie
		self.stop=False #okresla czy polaczenie jest 'przerywane'
		
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
		
		# testowe polaczenie:
		cl=xmpp.Client(jid.getDomain(),debug=[])
		if cl.connect() == "":
			print "not connected"
			sys.exit(0) 
		if cl.auth(jid.getNode(),pwd) == None: 
			print "authentication failed"
			sys.exit(0)
		self.connected=True
		#jesli polaczy sie w czasie krotszym niz pare sekund przyjmij
		#jako glowne polaczenie:
		if not self.active:	
			self.cl=cl
			
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
		
		#reset zmiennej stop
		self.stop=False
		
		gobject.idle_add(self.progress.show)

		self.i=0.00
		
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
			
		#jesli polaczenie bylo 'przerwane'
		if self.stop:
			#zrestartuj polaczenie
			threading.Thread(target=self.connecting,args=()).start()	

		#jesli minelo 25 i sie nie polaczyl i nie bylo reakcji usera
		if(str(self.i)=='1.0'):
			#wyswietl komunikat o bledzie
				self.toolong.hide()
				self.not_connected.show()
		
	#funkcje dla komunikatow
	def reconnect(self):
		self.stop=True
		self.toolong.hide()
	def reconnect2(self):
		self.not_connected.hide()
		threading.Thread(target=self.connecting,args=()).start()	

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
