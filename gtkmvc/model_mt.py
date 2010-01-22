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


from gtkmvc.model import Model
import support.metaclasses

try: import threading as _threading
except ImportError: import dummy_threading as _threading

import gobject
if hasattr(gobject, "threads_init"): gobject.threads_init()
else: import gtk; gtk.threads_init()


class ModelMT (Model):
    """A base class for models whose observable properties can be
    changed by threads different than gtk main thread. Notification is
    performed by exploiting the gtk idle loop only if needed,
    otherwise the standard notification system (direct method call) is
    used. In this model, the observer is expected to run in the gtk
    main loop thread."""

    __metaclass__  = support.metaclasses.ObservablePropertyMetaMT
    
    def __init__(self):
        Model.__init__(self)
        self.__observer_threads = {}
        self._prop_lock = _threading.Lock()
        return

    def register_observer(self, observer):
        Model.register_observer(self, observer)
        self.__observer_threads[observer] = _threading.currentThread()
        return

    def unregister_observer(self, observer):
        Model.unregister_observer(self, observer)
        del self.__observer_threads[observer]
        return

    # ---------- Notifiers:

    def __notify_observer__(self, observer, method, *args, **kwargs):
        """This makes a call either through the gtk.idle list or a
        direct method call depending whether the caller's thread is
        different from the observer's thread"""

        assert self.__observer_threads.has_key(observer)
        if _threading.currentThread() == self.__observer_threads[observer]:
            # standard call
            return Model.__notify_observer__(self, observer, method,
                                             *args, **kwargs)

        # multi-threading call
        gobject.idle_add(self.__idle_callback, observer, method, args, kwargs)
        return

    def __idle_callback(self, observer, method, args, kwargs):
        method(*args, **kwargs)
        return False


    pass # end of class


import gtk
# ----------------------------------------------------------------------
class TreeStoreModelMT (ModelMT, gtk.TreeStore):
    """Use this class as base class for your model derived by
    gtk.TreeStore"""
    __metaclass__  = support.metaclasses.ObservablePropertyGObjectMetaMT   
    
    def __init__(self, column_type, *args):
        ModelMT.__init__(self)
        gtk.TreeStore.__init__(self, column_type, *args)
        return
    pass


# ----------------------------------------------------------------------
class ListStoreModelMT (ModelMT, gtk.ListStore):
    """Use this class as base class for your model derived by
    gtk.ListStore"""
    __metaclass__  = support.metaclasses.ObservablePropertyGObjectMetaMT 
    
    def __init__(self, column_type, *args):
        ModelMT.__init__(self)
        gtk.ListStore.__init__(self, column_type, *args)
        return
    pass
    

# ----------------------------------------------------------------------
class TextBufferModelMT (ModelMT, gtk.TextBuffer):
    """Use this class as base class for your model derived by
    gtk.TextBuffer"""
    __metaclass__  = support.metaclasses.ObservablePropertyGObjectMetaMT 
    
    def __init__(self, table=None):
        ModelMT.__init__(self)
        gtk.TextBuffer.__init__(self, table)
        return
    pass
