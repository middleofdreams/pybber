
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
	style="default"
	
	__observables__=("pwd","login","remember")
	def __init__(self,):
		Model.__init__(self)
		self.tryfiles()
		
		

	def get_all(self):
		settings={"me":self.me,
				  "show":self.show,
				  "status":self.status,
				  "style":self.style}
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
		try: 
			self.style=d['style']
		except:
			self.style="default"	
			
		d.close()	
		
	def save(self,show,status,me,style):	
		
		d = gdbm.open(self.prefs, 'c')
		d['show']=str(show)
		d['status']=status
		self.show=show
		self.status=d['status']
		self.me=me
		d['me']=me
		print style
		workpath=os.environ['HOME']+"/pybber"
		stylepath=workpath+"/chatstyles/"+style
		print stylepath
		if not os.path.isdir(stylepath):
			style="default"
		self.style=style
		d['style']=style
		
		d.close()	
		
	def saveacc(self,remember,login,passwd):
		d = gdbm.open(self.prefs, 'c')
		d['login']=login
		if remember:
			d['pwd']=passwd
			d['remember']='True'
		else:
			d['pwd']=""
			d['remember']=""
		
		d.close()	

			
