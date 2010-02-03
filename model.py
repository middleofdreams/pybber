
import _importer,re
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
	settingtooltip=False
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
		nick=model[row][0]
		if "\n" in nick:
			n=nick.split("\n")
			nick=n[0]
		p = re.compile(r'<[^<]*?>')
		nick=p.sub(' ', nick)
		self.recipentname=nick
		self.recipent= model[row][4]
		
		


	pass # end of class

