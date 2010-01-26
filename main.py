if __name__ == "__main__":
 
	from model import MyModel
	from controller import MyCtrl
	from view import MyView
	from connection_ctrl import ConnectionCtrl
 
	m = MyModel()
	v = MyView()
	c = MyCtrl(m,v)
	cc = ConnectionCtrl(m.connection,v)
	import gtk
	gtk.main()
	pass
