
import _importer
from gtkmvc import Model
from connection_model import *
from settings_model import *
from archive_model import *
class MyModel (Model):
	"""Our model contains a numeric counter and a numeric value that
	holds the value that the counter must be assigned to when we the
	model is reset"""
	connection=ConnectionModel()
	archive=ArchiveModel()
	recipent=""
	recipentname=""
	archiveopen=""
	messages={}
	hidden=False
	newmessage=connection.newmessage
	newpresence=connection.newpresence
	archiveclose=archive.archiveclose
	__observables__ = ('recipent', 'archiveopen','messages', \
	'newmessage', 'newpresence',"archiveclose")
    

	def __init__(self):
		Model.__init__(self)

		self.settings=SettingsModel()
		self.observe_model(self.connection)
		self.observe_model(self.archive)
		return

	def openchat(self,widget, row, col):
		model = widget.get_model()
		self.recipentname=model[row][0]
		self.recipent= model[row][4]
		


	pass # end of class

