# -*- coding: utf-8 -*-
import _importer
from gtkmvc import Controller
from gtkmvc.adapters import Adapter
import time
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
		self.model.stop=True
		self.view['progress'].hide()
		self.view['jidlabel'].hide()
	def hidewarn(self,widget):
		self.view.hidewarn()
	
	def property_is_connecting_value_change(self, model, old, new):
		if new:
			self.view['progress'].show()
			self.view['jidlabel'].show()
		else:
			self.view['progress'].hide()
			self.view['toolong'].hide()
		return
	
	def property_connerror_value_change(self,model,old,new):
		if model.i<1.00:
			if new==model.tryid:
				model.stop=True
				self.view['not_connected'].show()
				self.view['errmessage'].show()
				login=self.view['login'].get_text()
				text="Sprawdź poprawność danych i połączenie z internetem"
				if not "@" in login or not "." in login:
					text+="\n Poprawny format hasla to: <b>nazwa@domena.com</b>"
				self.view['errmessage'].set_markup(text)
	def property_autherror_value_change(self,model,old,new):
		if model.i<1.00:
			if new:
				model.stop=True
				self.view['not_connected'].show()
				self.view['errmessage'].show()
				self.view['errmessage'].set_text("Hasło jest niepoprawne!")
				
				
	def property_i_value_change(self, model, old, new):
		#if new>old: self.view['progress'].show()

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
			time.sleep(0.2)
			self.view.create_empty_clist(items,self.model.roster,self.model.jid)
			
			#chowa ewentualne komunikaty
			self.view['toolong'].hide()
			self.view['not_connected'].hide()
			self.view['progress'].hide()
		else:
			self.view['listmodel'].clear()
			self.view['leftwindow'].hide()
		return
		pass # end of class
