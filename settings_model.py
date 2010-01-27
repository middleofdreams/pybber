
from gtkmvc import Model
import os,sys
import gdbm,gtk,pango



class SettingsModel(Model):
	dir=os.path.abspath(os.path.dirname(sys.argv[0]))+"/data"
	workpath=os.environ['HOME']+"/.pybber"
	prefs=workpath+"/prefs.db"
	pwd=""
	login=""
	remember=""
	
	__observables__=("pwd","login","remember")
	def __init__(self,):
		Model.__init__(self)
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

	def get_all(self):
		settings={"me":self.me,
				  "show":self.show,
				  "status":self.status}
		return settings
	def tryfiles(self):
		if not os.path.isdir(self.workpath):
			os.makedirs(self.workpath)
		d = gdbm.open(self.prefs, 'c')
		if d.firstkey()==None:
			d['show']=''
			d['status']="Pybber"
			d['me']="Me"
		d.close()
					
	def loadprefs(self):
		d = gdbm.open(self.prefs, 'r')
		show=d['show']
		try:
			self.show=int(show)
		except:
			self.show=1
		self.status=d['status']
		self.me=d['me']
		try:
			self.login=d['login']
			#
		except:
			self.login=None
		try:
			self.pwd=d['pwd']
			#mainclass.passwd.set_text(self.pwd)
		except:
			self.pwd=None
		try:
			self.remember=d['remember']
			#if remember=="True":
				#mainclass.wTree.get_widget('checkbutton1').set_active(True)
		except:
			pass		
			
		d.close()	
		
	def save(self,mainclass):	
		model = mainclass.wTree.get_widget('combobox2').get_model()
		active = mainclass.wTree.get_widget('combobox2').get_active()
		if active < 0:
		  show=0
		else:
			show=active
		d = gdbm.open(prefs, 'c')
		d['show']=str(show)
		d['status']=mainclass.wTree.get_widget('entry8').get_text()
		self.show=show
		self.status=d['status']
		me=mainclass.wTree.get_widget('entry11').get_text()
		if me=="":
			me=self.login
		self.me=me
		d['me']=me
		d.close()	
		print self.show
		
	def saveacc(self,mainclass):
		d = gdbm.open(prefs, 'c')
		d['login']=mainclass.login.get_text()
		remember=mainclass.wTree.get_widget('checkbutton1').get_active()
		if remember:
			d['pwd']=mainclass.passwd.get_text()
			d['remember']='True'
		else:
			d['pwd']=""
			d['remember']=""
		
		d.close()		
