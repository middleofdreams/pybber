import _importer
 
from gtkmvc import View
from listhelpers import get_show
from webkit import WebView
import gobject,gtk

class MainView (View):

	glade = "client.glade"

	def __init__(self):
		View.__init__(self)
		self['window'].set_title("Pybber")
		self['window'].show()
		self.createchat()
		self.hid=0
		self.createicon()

		
	def openchat(self):
		self['leftwindow'].show()
		
	def loadchat(self,html,style):
		css='<link rel=&#34;Stylesheet&#34; type=&#34;text/css&#34; href=&#34;chatstyles/'+style+'/main.css"&#34; /> '

		if html!="":
			if not "<link rel" in html:
				html=css+html
				print "aaa"
				print html
			self.hid=self['chat'].connect('load-finished',self.updatechat,html)
		else:
			if style!="default": 
				self.hid=self['chat'].connect('load-finished',self.updatechat,css)
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
		self['progress'].hide()
	def hidewarn(self):
		self['toolong'].hide()
	def reconnect(self):
		self['toolong'].hide()
		self['progress'].show()
		self['progress'].set_fraction(0)
		self['not_connected'].hide()
	def closesettings(self,mainh):
		self['window'].set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
		self['frame1'].hide()
		self['window'].resize(300,mainh)
	def opensettings(self,set):
		self['window'].set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
		self['frame1'].show()
		self['combobox2'].set_active(set['show'])
		self['entry8'].set_text(set['status'])
		self['entry11'].set_text(set['me'])
		self['chatstyle'].set_text(set['style'])
	def list_showform(self,form,prop=False,jid=None,name=None):
		self['list'].hide()
		self[form+'form'].show()	
		if prop:
			if jid!=None: self[form+'jid'].set_text(jid)
			if name!=None: self[form+'name'].set_text(name)
					
	def list_hideform(self,form):
		self[form+'form'].hide()
		self['list'].show()
		self[form+'jid'].set_text('')
		try: self[form+'name'].set_text('')
		except: pass
	def createicon(self):
		icon=gtk.status_icon_new_from_file("icons/pybber.png")
		icon.set_blinking(False) 
		icon.set_tooltip("Pybber")
		icon.set_visible(True)
		self.icon=icon
	def iconblink(self,blink=True):
		self.icon.set_blinking(blink)
	
	def archive_show(self):
		self['archivewindow'].show()
		self['archivelist'].show()
		self['archivescroll'].show()
		self['leftwindow'].show()
		self['archivelist'].get_model().clear()
		self['hbox3'].hide()
	def archive_addtolist(self,day,recipent):
		 self['archivelist'].get_model().append([day,recipent])
	def archive_showchat(self,html):
		self['chat'].load_html_string(html,"file:///")
	def archive_create(self):
		model=gtk.ListStore(gobject.TYPE_STRING,str)
		self['archivelist'].set_model(model)
		col=gtk.TreeViewColumn("Rozmowy:",gtk.CellRendererText(), text=0)
		self['archivelist'].append_column(col)
	def archive_close(self):
		self['archivewindow'].hide()
		self['archivelist'].hide()
		self['archivescroll'].hide()
		self['hbox3'].show()
	def message_newline(self):
		buffer=self['message'].get_buffer()
		buffer.insert_at_cursor(chr(13))	
