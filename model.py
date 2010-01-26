
import _importer
from gtkmvc import Model
from connection_model import *
from settings_model import *

class MyModel (Model):
	"""Our model contains a numeric counter and a numeric value that
	holds the value that the counter must be assigned to when we the
	model is reset"""
	connection=ConnectionModel()
	recipent=""
	recipentname=""
	archiveopen=""
	messages={}
	newmessage=connection.newmessage
	newpresence=connection.newpresence
	__observables__ = ('recipent', 'archiveopen','messages', \
	'newmessage', 'newpresence')
    

	def __init__(self):
		Model.__init__(self)

		self.settings=SettingsModel()
		self.observe_model(self.connection)
		return

	def openchat(self,widget, row, col):
		model = widget.get_model()
		self.recipent= model[row][4]
		self.recipentname=model[row][1]


	pass # end of class

