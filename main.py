if __name__ == "__main__":
 
	from model import MainModel
	from controller import MainCtrl
	from view import MainView
	from connection_ctrl import ConnectionCtrl
	from listmanage_ctrl import ListCtrl
	from archive_ctrl import ArchiveCtrl
    
	m = MainModel()
	v = MainView()
	c = MainCtrl(m,v)
	cc = ConnectionCtrl(m.connection,v)
	lc= ListCtrl(m,v)
	ac=ArchiveCtrl(m.archive,v)
	import gtk
	gtk.main()
	pass
