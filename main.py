if __name__ == "__main__":
 
	from model import MyModel
	from controller import MyCtrl
	from view import MyView
	from connection_ctrl import ConnectionCtrl
	from listmanage_ctrl import ListCtrl
	from archive_ctrl import ArchiveCtrl
    
	m = MyModel()
	v = MyView()
	c = MyCtrl(m,v)
	cc = ConnectionCtrl(m.connection,v)
	lc= ListCtrl(m,v)
	ac=ArchiveCtrl(m.archive,v)
	import gtk
	gtk.main()
	pass
