import _importer
 
from gtkmvc import View
from listhelpers import get_show
from webkit import WebView
import gobject,gtk
class MyView (View):

	glade = "client.glade"

	def __init__(self):
		View.__init__(self)
		self['window'].show()
		self.createchat()
		self.hid=0
		
	def openchat(self):
		self['leftwindow'].show()
		
	def loadchat(self,html):
		if html!="":
			self.hid=self['chat'].connect('load-finished',self.updatechat,html)
		self['chat'].load_uri('file:///home/kuba/pybber/chat.html')
		
	
	def updatechat(self,html,*a,**b):
		try:
			gobject.idle_add(self['chat'].execute_script,"appendtext('"+html+"');")
		except:
			gobject.idle_add(self['chat'].execute_script,"appendtext('"+a[1]+"');")
		if self.hid>0:
			self['chat'].disconnect(self.hid)
			self.hid=0
			
	def updatelist(self,item,status,show):		
		self['listmodel'].set_value(item,1,status)
		if self['listmodel'].get_value(item,3)!=None:
			self['listmodel'].set_value(item,3,get_show(show))
		else:
			self['listmodel'].set_value(item,2,get_show(show))
	
	def createchat(self):
		self['chat']=WebView()
		self['chatwindow'].add(self['chat'])
		self['chat'].show()
	def turn_desc_style(self,edit):	
		if not edit:
			color=gtk.gdk.color_parse("#D4D1C8")
		else:
			color=gtk.gdk.color_parse("#FFFFFF")
		self['desc'].modify_base(gtk.STATE_NORMAL,color)
		self['desc'].modify_base(gtk.STATE_ACTIVE,color)
		self['desc'].modify_base(gtk.STATE_PRELIGHT,color)
	def hide_chat(self,mainh):
		import gtk
		self['window'].set_title("Pybber")
		self['window'].set_gravity(gtk.gdk.GRAVITY_SOUTH_EAST)
		self['leftwindow'].hide()
		self['window'].resize(300,mainh)
		self['window'].present()
		self['archivewindow'].hide()
		self['archivelist'].hide()
		self['archivescroll'].hide()
		
	def changedata(self):
		self['toolong'].hide()
		self['loginbox'].show()
		self['not_connected'].hide()
	def hidewarn(self):
		self['toolong'].hide()
	def reconnect(self):
		self['toolong'].hide()
		self['progress'].show()
		self['progress'].set_fraction(0)
		self['not_connected'].hide()
