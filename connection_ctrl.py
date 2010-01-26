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
	def property_connecting_value_change(self, model, old, new):
		if new:
			self.view['progress'].show()
		else:
			self.view['progress'].hide()
			self.view['toolong'].hide()
		return
	
	def property_i_value_change(self, model, old, new):
		if new<1.000:
			self.view['progress'].set_fraction(new)
		if(str(new)=='0.15'):
				self.view['toolong'].show()
		if(str(new)=='1.0'):
			#wyswietl komunikat o bledzie
				self.view['toolong'].hide()
				if not self.model.active:
					self.view['not_connected'].show()
		return
		
		
	def property_active_value_change(self,model,old,new):
		#self.gui.staticon.set_from_file("icons/pybber.png") 
		if new:
			self.view['desc'].show()
			self.view['statusbar'].show()
			self.view['desc'].set_sensitive(1)
			self.view['statusbar'].set_sensitive(1)
			
			self.view['desc'].set_text(model.status)
			self.view['statusbar'].set_active(model.show)
			items=model.get_list()
			import list as clist
			clist.create_empty_list(self.view)		
			clist.get_all(items,self.view['listmodel'],self.model.roster)
			#chowa ewentualne komunikaty
			self.view['toolong'].hide()
			self.view['not_connected'].hide()
		return
		pass # end of class
