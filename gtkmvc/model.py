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
#  License along with this library; if not, write to the Free
#  Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.

import support.metaclasses
from support.wrappers import ObsWrapperBase
from observer import Observer
from observable import Signal
from support.log import logger

# these constants are used internally
_obs_implicit = 0
_obs_explicit = 1


class Model (Observer):
    """
    This class is the application model base class. It handles a set
    of observable properties which you are interested in showing by
    one ore more view - via one or more observers of course. The
    mechanism is the following:

    1. You are interested in showing a set of model property, that
       you can declare in the __properties__ member map.

    2. You define one or more observers that observe one or more
       properties you registered. When someone changes a property
       value the model notifies the changing to each observer.

    The property-observer[s] association is given by the implicit
    rule in observers method names: if you want the model notified
    the changing event of the value of the property 'p' you have to
    define the method called 'property_p_value_change' in each
    listening observer class.

    The Model is also an observer (typically, of itself and of
    other models. 
    
    Notice that tipically 'controllers' implement the observer
    pattern. The notification method gets the emitting model, the
    old value for the property and the new one.  Properties
    functionalities are automatically provided by the
    ObservablePropertyMeta meta-class."""

    __metaclass__  = support.metaclasses.ObservablePropertyMeta 
    __properties__ = {} # override this
    
    def __init__(self):
        Observer.__init__(self)
        
        self.__observers = []
        # keys are properties names, values are pairs (bool, methods)
        # inside the observer. bool is True for custom observing
        # methods, False otherwise
        self.__value_notifications = {}
        self.__instance_notif_before = {}
        self.__instance_notif_after = {}
        self.__signal_notif = {}
        
        for key in self.get_properties(): self.register_property(key)
        return

    def register_property(self, name):
        """Registers an existing property to be monitored, and sets
        up notifiers for notifications"""
        if not self.__value_notifications.has_key(name): 
            self.__value_notifications[name] = []
            pass
        
        # registers observable wrappers
        prop = getattr(self, "_prop_%s" % name, None)
            
        if isinstance(prop, ObsWrapperBase):
            prop.__set_model__(self, name)

            if isinstance(prop, Signal):
                if not self.__signal_notif.has_key(name):
                    self.__signal_notif[name] = []
                    pass
                pass
            else:
                if not self.__instance_notif_before.has_key(name):
                    self.__instance_notif_before[name] = []
                    pass
                if not self.__instance_notif_after.has_key(name):
                    self.__instance_notif_after[name] = []
                    pass
                pass
            pass
                
        return


    def has_property(self, name):
        """Returns true if given property name refers an observable
        property inside self or inside derived classes"""
        return name in self.get_properties()


    def register_observer(self, observer):
        """Register given observer among those observers which are
        interested in observing the model"""
        if observer in self.__observers: return # not already registered

        assert isinstance(observer, Observer)
        self.__observers.append(observer)
        for key in self.get_properties():
            self.__add_observer_notification(observer, key)
            pass
        
        return
            

    def unregister_observer(self, observer):
        """Unregister the given observer that is no longer interested
        in observing the model"""
        assert isinstance(observer, Observer)

        if observer not in self.__observers: return
        for key in self.get_properties():
            self.__remove_observer_notification(observer, key)
            pass
        
        self.__observers.remove(observer) 
        return


    def _reset_property_notification(self, prop_name):
        """Called when it has be done an assignment that changes the
        type of a property or the instance of the property has been
        changed to a different instance. In this case it must be
        unregistered and registered again"""

        self.register_property(prop_name)

        for observer in self.__observers:
            self.__remove_observer_notification(observer, prop_name)
            self.__add_observer_notification(observer, prop_name)
            pass
        return
    

    def get_properties(self):
        """Returns a list of all observable properties accessible
        from the model"""
        return list(getattr(self, support.metaclasses.ALL_OBS_SET, []))

    
    def __add_observer_notification(self, observer, prop_name):
        """Searches in the observer for any possible listener, and
        stores the notification methods to be called later"""

        # retrieves the set of custom observing methods 
        cust_methods = observer.get_custom_observing_methods(prop_name)

        method_name = "property_%s_value_change" % prop_name
        if hasattr(observer, method_name):
            pair = (_obs_implicit, getattr(observer, method_name))
            if pair not in self.__value_notifications[prop_name]:
                list.append(self.__value_notifications[prop_name], pair)
                logger.debug("Added implicit value change notification '%s'",
                             method_name)
                pass
            pass

        # checks for custom observing methods. If it is a signal,
        # a method or value is decided from number of
        # arguments. This is not particularly robust.
        # self, model, prop_name, old, new
        for meth in (m for m in cust_methods
                     if m.im_func.func_code.co_argcount == 5):
                
            pair = (_obs_explicit, meth)
            if pair not in self.__value_notifications[prop_name]:
                list.append(self.__value_notifications[prop_name], pair)
                logger.debug("Added explicit value change notification '%s'",
                             meth.im_func.__name__)
                pass
            pass

        # is it a signal?
        orig_prop = getattr(self, "_prop_%s" % prop_name, None)
        if isinstance(orig_prop, Signal):
            method_name = "property_%s_signal_emit" % prop_name
            if hasattr(observer, method_name):
                pair = (_obs_implicit, getattr(observer, method_name))
                if pair not in self.__signal_notif[prop_name]:
                    list.append(self.__signal_notif[prop_name], pair)
                    logger.debug("Added implicit signal emit notification '%s'",
                                 method_name)
                    pass
                pass

            # checks for custom observing methods. If it is a signal,
            # a method or value is decided from number of
            # arguments. This is not particularly robust.
            # self, model, signal_name, arg
            for meth in (m for m in cust_methods
                         if m.im_func.func_code.co_argcount == 4):
                
                pair = (_obs_explicit, meth)
                if pair not in self.__signal_notif[prop_name]:
                    list.append(self.__signal_notif[prop_name], pair)
                    logger.debug("Added explicit signal emit notification '%s'",
                                 meth.im_func.__name__)
                    pass
                pass                    
            pass
        
        # is it an instance change notification type?
        elif isinstance(orig_prop, ObsWrapperBase):
            method_name = "property_%s_before_change" % prop_name
            if hasattr(observer, method_name):
                pair = (_obs_implicit, getattr(observer, method_name))
                if pair not in self.__instance_notif_before[prop_name]:
                    list.append(self.__instance_notif_before[prop_name], pair)
                    logger.debug("Added implicit before call notification '%s'",
                                 method_name)
                    pass
                pass

            # checks for custom observing methods. If it is a signal,
            # a method or value is decided from number of
            # arguments. This is not particularly robust.
            # self, model, prop_name, instance, meth_name, args, kwargs
            for meth in (m for m in cust_methods
                         if m.im_func.func_code.co_argcount == 7):
                
                pair = (_obs_explicit, meth)
                if pair not in self.__instance_notif_before[prop_name]:
                    list.append(self.__instance_notif_before[prop_name], pair)
                    logger.debug("Added explicit before call notification '%s'",
                                 meth.im_func.__name__)
                    pass
                pass                    

            method_name = "property_%s_after_change" % prop_name
            if hasattr(observer, method_name):
                pair = (_obs_implicit, getattr(observer, method_name))
                if pair not in self.__instance_notif_after[prop_name]:
                    list.append(self.__instance_notif_after[prop_name], pair)
                    logger.debug("Added implicit after call notification '%s'",
                                 method_name)
                    pass
                pass

            # checks for custom observing methods. If it is a signal,
            # a method or value is decided from number of
            # arguments. This is not particularly robust.
            # self, model, prop_name, instance, meth_name, res, args, kwargs
            for meth in (m for m in cust_methods
                         if m.im_func.func_code.co_argcount == 8):
                
                pair = (_obs_explicit, meth)
                if pair not in self.__instance_notif_after[prop_name]:
                    list.append(self.__instance_notif_after[prop_name], pair)
                    logger.debug("Added explicit after call notification '%s'",
                                 meth.im_func.__name__)
                    pass
                pass                    
            
            pass

        return

    
    def __remove_observer_notification(self, observer, prop_name):

        # retrieves the set of custom observing methods
        # and removes corresponding the notification methods
        cust_methods = observer.get_custom_observing_methods(prop_name)
        for meth in cust_methods:
            pair = (_obs_explicit, meth)
            for _map in (self.__value_notifications,
                         self.__signal_notif,
                         self.__instance_notif_before,
                         self.__instance_notif_after,):
                         
                if prop_name in _map and \
                        pair in _map[prop_name]: _map[prop_name].remove(pair)
                pass
            pass
            
        if self.__value_notifications.has_key(prop_name):
            method_name = "property_%s_value_change" % prop_name
            if hasattr(observer, method_name):
                pair = (_obs_implicit, getattr(observer, method_name))
                if pair in self.__value_notifications[prop_name]:
                    self.__value_notifications[prop_name].remove(pair)
                    logger.debug("Removed implicit value change notification '%s'",
                                 method_name)
                    pass
                pass
            pass


        orig_prop = getattr(self, "_prop_%s" % prop_name, None)
        # is it a signal?
        if isinstance(orig_prop, Signal):
            method_name = "property_%s_signal_emit" % prop_name
            if hasattr(observer, method_name):
                pair = (_obs_implicit, getattr(observer, method_name))
                if pair in self.__signal_notif[prop_name]:
                    self.__signal_notif[prop_name].remove(pair)
                    logger.debug("Removed implicit signal emit notification '%s'",
                                 method_name)
                    pass
                pass
            pass

        # is it an instance change notification type?
        elif isinstance(orig_prop, ObsWrapperBase):
            if self.__instance_notif_before.has_key(prop_name):
                method_name = "property_%s_before_change" % prop_name
                if hasattr(observer, method_name):
                    pair = (_obs_implicit, getattr(observer, method_name))
                    if pair in self.__instance_notif_before[prop_name]:
                        self.__instance_notif_before[prop_name].remove(pair)
                        logger.debug("Removed implicit before call "\
                                         "notification '%s'", method_name)
                        pass
                    pass
                pass
            
            if self.__instance_notif_after.has_key(prop_name):
                method_name = "property_%s_after_change" % prop_name
                if hasattr(observer, method_name):
                    pair = (_obs_implicit, getattr(observer, method_name))
                    if pair in self.__instance_notif_after[prop_name]:
                        self.__instance_notif_after[prop_name].remove(pair)
                        logger.debug("Removed after call notification '%s'",
                                     method_name)
                        pass
                    pass
                pass
            pass
            
        return 


    def __notify_observer__(self, observer, method, *args, **kwargs):
        """This can be overridden by derived class in order to call
        the method in a different manner (for example, in
        multithreading, or a rpc, etc.)  This implementation simply
        calls the given method with the given arguments"""
        return method(*args, **kwargs)
    
    # -------------------------------------------------------------
    #            Notifiers:
    # -------------------------------------------------------------
    
    def notify_property_value_change(self, prop_name, old, new):
        assert(self.__value_notifications.has_key(prop_name))
        for flag, method in self.__value_notifications[prop_name] :
            obs = method.im_self
            # notification occurs checking spuriousness of the observer
            if old != new or obs.accepts_spurious_change():
                if flag == _obs_implicit: 
                    self.__notify_observer__(obs, method,
                                             self, old, new) # notifies the change
                else: # explicit (custom) notification
                    self.__notify_observer__(obs, method,
                                             self, prop_name, old, new) # notifies the change
                    pass
                pass
            pass
        return                

    def notify_method_before_change(self, prop_name, instance, meth_name,
                                    args, kwargs):
        assert(self.__instance_notif_before.has_key(prop_name))
        for flag, method in self.__instance_notif_before[prop_name]:
            # notifies the change
            if flag == _obs_implicit: 
                self.__notify_observer__(method.im_self, method,
                                         self, instance,
                                         meth_name, args, kwargs)
            else: # explicit (custom) notification
                self.__notify_observer__(method.im_self, method,
                                         self, prop_name, instance,
                                         meth_name, args, kwargs)
            pass
        return                

    def notify_method_after_change(self, prop_name, instance, meth_name,
                                   res, args, kwargs):
        assert(self.__instance_notif_after.has_key(prop_name))
        for flag, method in self.__instance_notif_after[prop_name]:
            # notifies the change
            if flag == _obs_implicit: 
                self.__notify_observer__(method.im_self, method,
                                         self, instance,
                                         meth_name, res, args, kwargs) 
            else: # explicit (custom) notification
                self.__notify_observer__(method.im_self, method,
                                         self, prop_name, instance,
                                         meth_name, res, args, kwargs)
            
            pass
        return

    def notify_signal_emit(self, prop_name, arg):
        assert(self.__signal_notif.has_key(prop_name))
        
        for flag, method in self.__signal_notif[prop_name]:
            # notifies the signal emit
            if flag == _obs_implicit:
                self.__notify_observer__(method.im_self, method,
                                         self, arg)
            else: # explicit (custom) notification
                self.__notify_observer__(method.im_self, method,
                                         self, prop_name, arg)
            pass
        return
        

    pass # end of class Model
# ----------------------------------------------------------------------



import gtk
# ----------------------------------------------------------------------
class TreeStoreModel (Model, gtk.TreeStore):
    """Use this class as base class for your model derived by
    gtk.TreeStore"""
    __metaclass__  = support.metaclasses.ObservablePropertyGObjectMeta   
    
    def __init__(self, column_type, *args):
        gtk.TreeStore.__init__(self, column_type, *args)
        Model.__init__(self)
        return
    pass


# ----------------------------------------------------------------------
class ListStoreModel (Model, gtk.ListStore):
    """Use this class as base class for your model derived by
    gtk.ListStore"""
    __metaclass__  = support.metaclasses.ObservablePropertyGObjectMeta   
    
    def __init__(self, column_type, *args):
        gtk.ListStore.__init__(self, column_type, *args)
        Model.__init__(self)
        return
    pass
    

# ----------------------------------------------------------------------
class TextBufferModel (Model, gtk.TextBuffer):
    """Use this class as base class for your model derived by
    gtk.TextBuffer"""
    __metaclass__  = support.metaclasses.ObservablePropertyGObjectMeta   
    
    def __init__(self, table=None):
        gtk.TextBuffer.__init__(self, table)
        Model.__init__(self)
        return
    pass
    


# ----------------------------------------------------------------------
try:
  __connection__ = "sqlite:/:memory:"
  from sqlobject.inheritance import InheritableSQLObject
  class SQLObjectModel (InheritableSQLObject, Model):
      __metaclass__ = support.metaclasses.ObservablePropertyMetaSQL

      def __init__(self, *args, **kargs):
          InheritableSQLObject.__init__(self, *args, **kargs)
          Model.__init__(self)
          return
      pass # end of class
  SQLObjectModel.createTable()
except: pass
