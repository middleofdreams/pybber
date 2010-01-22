#  Author: Roberto Cavada <cavada@fbk.eu>
#
#  Copyright (c) 2006 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.


import _importer
from gtkmvc import Controller


class MyCtrl (Controller):
	"""Handles signal processing, and keeps alignment of model and
	view"""
	def __init__(self, model, view):  
		Controller.__init__(self, model, view)  
		return  
	def register_view(self, view):
		# sets initial values for the view
		return

		# gtk signals
	def on_window_delete_event(self, window, event):
		import gtk
		gtk.main_quit()
		return True

	def on_logonbtn_clicked(self,button):
		print "aaa"
		jid=self.view['login'].get_text()
		pwd=self.view['passwd'].get_text()
		self.model.connection.connect_init(jid,pwd)
		#self.settings.saveacc(self)
		self.view['loginbox'].hide()
		self.view['jidlabel'].set_label(jid)	
		
		#self.staticon.set_from_file("icons/disconnected.png") 
		return

	

		# observable properties    
	def property_counter_value_change(self, model, old, new):
		self.view.set_counter_value(new)
		return
		
	def property_connecting_value_change(self, model, old, new):
		self.view['progressbar'].show()
		return

		pass # end of class
