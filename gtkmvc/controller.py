#  Author: Roberto Cavada <cavada@fbk.eu>
#
#  Copyright (c) 2005 by Roberto Cavada
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


from gtkmvc.observer import Observer
import types
import gobject

class Controller (Observer):
    """
    We put all of our gtk signal handlers into a class.  This lets
    us bind all of them at once, because their names are in the
    class dict.  This class automatically register its instances as
    observers into the corresponding model.  Also, when a view is
    passed, method register_view got called, which can be
    oveloaded in order to connect signals and perform other specific
    operation. A controller possibly handles and contains also a set
    of adapters that makes easier to connect widgets and observable
    properties into the model.

    parameter spurious controls the way spurious value change
    notifications are handled. If True, assignments to observable
    properties that do not actually change the value are
    notified anyway."""

    def __init__(self, model, view=None, spurious=False, auto_adapt=False):
        Observer.__init__(self, model, spurious)

        self.model = model
        self.view = None
        self.__adapters = []
        # set of properties explicitly adapted by the user:
        self.__user_props = set()
        self.__auto_adapt = auto_adapt
        
        if view: gobject.idle_add(self._idle_register_view, view, priority=gobject.PRIORITY_HIGH)
        return

    def _idle_register_view(self, view):
        """Internal method that calls register_view"""
        assert(self.view is None)
        self.view = view

        self.__autoconnect_signals()

        self.register_view(view)
        self.register_adapters()
        if self.__auto_adapt: self.adapt()
        return False

    def register_view(self, view):
        """
        This method is called by the framework when registering a
        view. Derived classes can exploit this call to connect
        signals manually, create and connect treeview, textview,
        etc.
        """
        assert(self.model is not None)
        assert(self.view is not None)
        return

    def register_adapters(self):
        """
        This method is called by register_view during view
        registration process, when it is time to possibly create all
        adapters. model and view can safely be taken from self.model
        and self.view. Derived classes can specilize this method. In
        this implementation the method does auto-adaptation if
        requested.
        """
        assert(self.model is not None)
        assert(self.view is not None)
        return

    def adapt(self, *args):
        """
        Adapts a set of (observable) properties and a set of
        widgets, by connecting them.

        This method can be used to simplify the creation of one or
        more adapters, by letting the framework do most of the work
        needed to connect ('adapt') properties from one hand, and
        widgets on the other.

        This method is provided in four flavours:

        1. No arguments. All properties in observed model will be
           checked for possible widgets to be adapted with.

        2. An instance of an Adapter class can be created by the
           caller and passed as a unique argument. The adapter must
           be already fully configured.

        3. The name of a model's property is passed as a unique
           argument.  A correponding widget name is searched and if
           found, an adapter is created. Name matching is performed
           by searching into view's widget names for words that end
           with the given property name. Matching is case
           insensitive and words can be separated by spaces,
           underscore (_) and CapitalizedWords. For example property
           'prop' will match widget 'cb_prop'. If no matches or
           multiple matches are found, a ValueError will be raised.
           The way names are matched can be customized by deriving
           method match_prop_name.

        4. Two strings can be passed, respectively containing the
           name of an observable property in the model, and the name
           of a widget in the view.

        Flavour 2 allows for a full control, but flavour 1, 3 and 4
        make easier to create adpaters with basic (default)
        behaviour.

        This method can be called into the method register_adapters
        which derived classes can specialise.
        """
        
        # checks arguments
        n = len(args)
        if n not in range(3): raise TypeError("adapt() takes 0, 1 or 2 arguments (%d given)" % n)

        if n==0:
            adapters = []
            props = self.model.get_properties()
            # matches all properties not previoulsy adapter by the user:
            for prop_name in filter(lambda p: p not in self.__user_props, props):
                wid_name = self.__find_widget_match(prop_name)
                #print "Auto-adapting property",prop_name, "and widget", wid_name
                adapters += self.__create_adapters__(prop_name, wid_name)                
                pass

        elif n == 1: #one argument
            from gtkmvc.adapters.basic import Adapter
            
            if isinstance(args[0], Adapter): adapters = (args[0],)

            elif isinstance(args[0], types.StringType):
                prop_name = args[0]
                wid_name = self.__find_widget_match(prop_name)
                adapters = self.__create_adapters__(prop_name, wid_name)
                pass
            else: raise TypeError("Argument of adapt() must be an Adapter or a string")

        else: # two arguments
            if not (isinstance(args[0], types.StringType) and
                    isinstance(args[1], types.StringType)):
                raise TypeError("Arguments of adapt() must be two strings")

            # retrieves both property and widget, and creates an adapter
            prop_name, wid_name = args
            adapters = self.__create_adapters__(prop_name, wid_name)
            pass

        for ad in adapters:
            self.__adapters.append(ad)
            # remember properties added by the user
            if n > 0: self.__user_props.add(ad.get_property_name())
            pass
        
        return

    def __find_widget_match(self, prop_name):
        """Given a property name, searches into the view for a
        possible corresponding widget to adapt with. This is called by
        adapt. Returns the matching candidate widget name"""

        names = []
        for wid_name in self.view:
            # if widget names ends with given property name: we skip
            # any prefix in widget name
            if wid_name.lower().endswith(prop_name.lower()): names.append(wid_name)
            pass

        if len(names) != 1:
            raise ValueError("%d widget candidates match property '%s': %s" % \
                                 (len(names), prop_name, names))
        
        return names[0]

        
    # performs Controller's signals auto-connection:
    def __autoconnect_signals(self):
        """This is called during view registration, to autoconnect
        signals in glade file with methods within the controller"""
        dic = {}
        for name in dir(self):
            method = getattr(self, name)
            if (not callable(method)): continue
            assert(not dic.has_key(name)) # not already connected!
            dic[name] = method
            pass

        for xml in self.view.xmlWidgets: xml.signal_autoconnect(dic) 
        return

    
    def __match_prop_name(self, prop_name, wid_name):
        """
        Used internally when searching for a suitable widget. To customize
        its behaviour, re-implement this method into derived classes
        """
        return 


    def __create_adapters__(self, prop_name, wid_name):
        """
        Private service that looks at property and widgets types,
        and possibly creates one or more (best) fitting adapters
        that are returned as a list.
        """
        from gtkmvc.adapters.basic import Adapter, RoUserClassAdapter
        from gtkmvc.adapters.containers import StaticContainerAdapter
        import gtk

        res = []

        wid = self.view[wid_name]
        if wid is None: raise ValueError("Widget '%s' not found" % wid_name)

        # Decides the type of adapters to be created.
        if isinstance(wid, gtk.Calendar):
            # calendar creates three adapter for year, month and day
            ad = RoUserClassAdapter(self.model, prop_name,
                                    lambda d: d.year, lambda d,y: d.replace(year=y))
            ad.connect_widget(wid, lambda c: c.get_date()[0],
                              lambda c,y: c.select_month(c.get_date()[1], y),
                              "day-selected")
            res.append(ad) # year
            
            ad = RoUserClassAdapter(self.model, prop_name,
                                    lambda d: d.month, lambda d,m: d.replace(month=m))
            ad.connect_widget(wid, lambda c: c.get_date()[1]+1,
                              lambda c,m: c.select_month(m-1, c.get_date()[0]),
                              "day-selected")
            res.append(ad) # month

            ad = RoUserClassAdapter(self.model, prop_name,
                                  lambda d: d.day, lambda d,v: d.replace(day=v))
            ad.connect_widget(wid, lambda c: c.get_date()[2],
                              lambda c,d: c.select_day(d),
                              "day-selected")
            res.append(ad) # day
            return res

            
        try: # tries with StaticContainerAdapter
            ad = StaticContainerAdapter(self.model, prop_name)
            ad.connect_widget(wid)
            res.append(ad)
            
        except TypeError:
            # falls back to a simple adapter
            ad = Adapter(self.model, prop_name)
            ad.connect_widget(wid)
            res.append(ad)
            pass

        return res

                            
    pass # end of class Controller
