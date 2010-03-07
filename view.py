# -*- coding: utf-8 -*-
import _importer
 
from gtkmvc import View
from listhelpers import get_show
from webkit import WebView
import gobject,gtk
import sys, os,pynotify

         
pathname = os.path.dirname(sys.argv[0])        
path= os.path.abspath(pathname)
class MainView (View):

	glade = "client.glade"

	def __init__(self):
		View.__init__(self)
		self['window'].set_title("Pybber")
		self['window'].show()
		self['window'].set_icon_from_file(path+"/icons/pybber.png")
		self['chatstyle']=gtk.combo_box_new_text()
		self['hbuttonbox4'].add(self['chatstyle'])
		self['chatstyle'].show_all()
		self.createchat()
		self.hid=0
		self.createicon()
		self['stylevarslist']=gtk.combo_box_new_text()
		self['stylevarsbox'].add(self['stylevarslist'])
		self['stylevarslist'].show_all()
		self['window'].set_role("Pybber")
		
	def openchat(self):
		self['leftwindow'].show()
		
	def loadchat(self,html,style,template=False,variant=""):
		if variant!="":	
			variant='<link href="Variants/'+variant+'.css" rel="stylesheet" type="text/css">'

			if html!="":
				html=variant+html
			else:
				html=variant
				
		if html!="":
			self.hid=self['chat'].connect('load-finished',self.updatechat,html,False)

		if not template:
			self['chat'].load_uri('file://'+path+'/chatstyles/default/Template.html')
		else:
			self['chat'].load_uri('file://'+path+'/chatstyles/'+style+'/Template.html')

		gobject.idle_add(self['message'].grab_focus)
	
	def updatechat(self,html,a=None,html2=None,continous=False,):
		if continous:
			script="NextMessage"
		else:
			script="Message"
		try:
			gobject.idle_add(self['chat'].execute_script,"append"+script+"('"+html+"');")
			
		except:
			gobject.idle_add(self['chat'].execute_script,"append"+script+"('"+html2+"');")
			gobject.idle_add(self['chat'].execute_script,"alignChat(true)")

		if self.hid>0:
			self['chat'].disconnect(self.hid)
			self.hid=0

	def updatelist(self,item,status,show):		
		self['listmodel'].set_value(item,0,status)
		show,priority=get_show(show)
		if self['listmodel'].get_value(item,3)!=None:
			self['listmodel'].set_value(item,3,show)
			self['listmodel'].set_value(item,5,priority+20)
		else:
			self['listmodel'].set_value(item,2,show)
			self['listmodel'].set_value(item,5,priority)
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
	def opensettings(self,set,styles,stylevars):
		self['window'].set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
		self['frame1'].show()
		self['combobox2'].set_active(set['show'])
		self['entry8'].set_text(set['status'])
		self['entry11'].set_text(set['me'])
		self['chatstyle'].get_model().clear()

		self['chatstyle'].get_model().append([set['style']])
		self['chatstyle'].set_active(0)
		for i in styles:
			if i!=set['style']:
				self['chatstyle'].get_model().append([i])
		if set['notify1']=="True":self['notify1'].set_active(True)	
		if set['notify2']=="True":self['notify2'].set_active(True)		
		self['stylevarslist'].get_model().clear()

		if stylevars!="":
			self['stylevarsbox'].set_sensitive(1)
			if set['stylevar']!="":
				self['stylevarslist'].get_model().append([set['stylevar']])
				self['stylevarscheck'].set_active(True)
			for i in stylevars:
				if i.endswith(".css"):
					i=i.rstrip(".css")
					if i!=set['stylevar']:
						self['stylevarslist'].get_model().append([i])
			self['stylevarslist'].set_active(0)

			
				
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
		self['vbox8'].hide()
	def archive_addtolist(self,day,recipent):
		 self['archivelist'].get_model().append([day,recipent])
	def archive_showchat(self,html):
		self['chat'].load_html_string(html,'file:///')
	def archive_create(self):
		model=gtk.ListStore(gobject.TYPE_STRING,str)
		self['archivelist'].set_model(model)
		col=gtk.TreeViewColumn("Rozmowy:",gtk.CellRendererText(), text=0)
		self['archivelist'].append_column(col)
	def archive_close(self):
		self['archivewindow'].hide()
		self['archivelist'].hide()
		self['archivescroll'].hide()
		self['vbox8'].show()
	def message_newline(self):
		buffer=self['message'].get_buffer()
		buffer.insert_at_cursor(chr(13))
	def create_empty_clist(self,items,roster,jid):
		import list as clist
		clist.create_empty_list(self)
		index=self['statusbar'].get_active()
		if index==0:
			show= None
		if index==1:
			show= "away"
		if index==2:
			show= "xa"
		if index==3:
			show= "dnd"
		if index==4:
			show= "chat"
		if index==5:
			show= "unavailable"
		desc=self['desc'].get_text()
		clist.get_all(items,self['listmodel'],roster,jid,desc,show)	
	def notification(self,user,text):
		title="Nowa wiadomość od "+user
		try:
			self.n.update(title=title,body=text)
		except:
			self.n = pynotify.Notification(title, text)  
			#self.n.attach_to_status_icon(self.icon)
		self.n.show()
	def create_style_variants(self,vlist):
		self['stylevarsbox'].set_sensitive(1)
		for i in vlist:
			self['stylevarslist'].get_model().append([i])
		self['stylevarslist'].set_active(0)
	def align_chat(self):
		gobject.idle_add(self['chat'].execute_script,"alignChat(true)")
