# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pygtk,gtk,xmpp,threading,time,xmpp,gobject,sys

class connection(threading.Thread):
	def __init__(self,guiclass):
		#self.gui=guiclass
		self.desc=guiclass.desc
		threading.Thread.__init__(self)
		threading.Thread(target=self.connecting,args=()).start()
		self.progress=guiclass.progress

	def connecting(self):
		self.ifrun=True
		threading.Thread(target=self.connectbar,args=()).start()

		jid = 'pybberclient@gmail.com' # @gmail.com 
		pwd   = 'pybberjabber'
		jid=xmpp.protocol.JID(jid)  
		self.cl=xmpp.Client(jid.getDomain(),debug=[])
		if self.cl.connect() == "":
			print "not connected"
			sys.exit(0) 
		if self.cl.auth(jid.getNode(),pwd) == None: 
			print "authentication failed"
			sys.exit(0)
		self.ifrun=False
		self.cl.send(xmpp.dispatcher.Presence(priority=5, show=None,status="Pybber test"))
		self.desc.set_text("Pybber test")
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


