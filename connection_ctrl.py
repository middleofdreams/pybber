import _importer
from gtkmvc import Controller
from gtkmvc.adapters import Adapter

class ConnectionCtrl (Controller):
	"""Handles signal processing, and keeps alignment of model and
	view"""

	def register_view(self, view):
		# sets initial values for the view
		return
	def register_adapters(self):
		ad = Adapter(self.model, "jid")
		ad.connect_widget(self.view["jidlabel"])
	def reconnect(self,widget):
		self.model.reconnect()
		self.view.reconnect()
		#self.on_logonbtn_clicked(widget)
	def changedata(self, *widget):
		self.view.changedata()
		self.model.is_connecting=False
	def hidewarn(self,widget):
		self.view.hidewarn()
	
	def property_is_connecting_value_change(self, model, old, new):
		print new
		if new:
			self.view['progress'].show()
		else:
			self.view['progress'].hide()
			self.view['toolong'].hide()
		return
	
	def property_i_value_change(self, model, old, new):
		self.view['progress'].show()
		if new<1.000:
			self.view['progress'].set_fraction(new)
		if(str(new)=='0.15'):
				self.view['toolong'].show()
		if(str(new)=='1.0'):
			#wyswietl komunikat o bledzie
				self.view['toolong'].hide()
				if not self.model.active:
					self.view['not_connected'].show()
					self.view['progress'].hide()
		return
		
		
	def property_active_value_change(self,model,old,new):
		if new:
			self.view['desc'].show()
			self.view['statusbar'].show()
			self.view['desc'].set_sensitive(1)
			self.view['statusbar'].set_sensitive(1)
			
			self.view['desc'].set_text(model.status)
			self.view['statusbar'].set_active(model.show)
			items=model.get_list()
			self.view.create_empty_clist(items,self.model.roster)
			
			#chowa ewentualne komunikaty
			self.view['toolong'].hide()
			self.view['not_connected'].hide()
			self.view['progress'].hide()
		else:
			self.view['listmodel'].clear()
			self.view['leftwindow'].hide()
		return
		pass # end of class
