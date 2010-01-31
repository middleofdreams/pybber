
import _importer
from gtkmvc import Model
from connection_model import *
from settings_model import *
from archive_model import *
class MainModel (Model):
	connection=ConnectionModel()
	archive=ArchiveModel()
	recipent=""
	recipentname=""
	archiveopen=""
	messages={}
	hidden=False
	messagetype={}
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

