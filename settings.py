

import os,sys
import gdbm,gtk,pango


dir=os.path.abspath(os.path.dirname(sys.argv[0]))+"/data"
workpath=os.environ['HOME']+"/.pybber"
prefs=workpath+"/prefs.db"


class settings():
	def __init__(self):
		self.tryfiles()
			
	def openwindow(self,mainclass):
		#if not mainclass.notifies:
		#	mainclass.wTree.get_widget("label9").set_sensitive(False)
		#	mainclass.wTree.get_widget("vbox8").set_sensitive(False)
		#	mainclass.wTree.get_widget("label11").set_text("Install python-notify \nto get this work!")
		#	mainclass.wTree.get_widget("label11").modify_font(pango.FontDescription("sans 17")) 
		#response = mainclass.prefwindow.run() 	
		#if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
		#	mainclass.prefwindow.hide()

		pass


	def tryfiles(self):
		if not os.path.isdir(workpath):
			os.makedirs(workpath)
		d = gdbm.open(prefs, 'c')
		if d.firstkey()==None:
			d['show']=''
			d['status']="Pybber"
			d['me']="Me"
		d.close()
					
	def loadprefs(self,mainclass):
		d = gdbm.open(prefs, 'r')
		self.show=d['show']
		self.status=d['status']
		self.me=d['me']
		try:
			self.login=d['login']
			mainclass.login.set_text(self.login)
		except:
			self.login=None
		try:
			self.pwd=d['pwd']
			mainclass.passwd.set_text(self.pwd)

		except:
			self.pwd=None
			
		d.close()	
	def saveprefs(self,mainclass):
				
		
		d = gdbm.open(prefs, 'c')
		d["action"]=str(action)
		d["minutes"]=str(time)
		d["hours"]=str(timeh)
		d["closeapp"]=str(closeapp)
		d["runbefore"]=str(runbefore)
		d["userdata1"]=str(puserdata)
		d["userdata2"]=str(puserdata2)
		d.close()	
		
	def saveacc(self,mainclass):
		d = gdbm.open(prefs, 'c')
		d['login']=mainclass.login.get_text()
		d['pwd']=mainclass.passwd.get_text()
		d.close()		
	
