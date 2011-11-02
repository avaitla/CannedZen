from CannedZen.Utils.Base_Utilities import default_app_path, try_delete_path
import os, copy

# This Class Provides A Container for storing various
# packages and relevant categories those packages may
# fall into. In general we build one of these, and then
# we simply use registerPackage with that object.
class EngineRegistrarObject(object):
    def __init__(self):
        self.categories = {}
        self.packages = {}
        self.classFactories = {}
    
    def registerPackage(self, engine, name, categories=[]):
        assert name not in self.packages, "Name %s Already Exists in Packages" % name
        self.packages[name] = engine
        for category in categories:
            self.categories.setdefault(category, []).append(name)

    def getPackage(self, name):
        return self.packages[name]

EngineRegistrar = EngineRegistrarObject()


# Decorator for Registering an Engine
# This is not really used anywhere, but it means that
# we can register an engine or interact without
# having to use the metaclass inheritance
def registerEngine(cls):
    EngineRegistrar.registerPackage(cls, cls.__name__, cls.categories)

# If we want to register a factory, we'll have to go this method
def registerEngineFactory(func, name):
    EngineRegistrar.classFactories[name] = func


class RegisterEngine(type):
    def __init__(cls, name, bases, dct):
        super(RegisterEngine, cls).__init__(name, bases, dct)
        if(name != "BaseEngine"): registerEngine(cls)

# This is the Base Class for a Plug and Play Component
# The functions listed are mostly left as interface methods
# which should be reimplemented by items inherting this
# base class. It should not be used unless inherited
# All internal methods must be idempotent, as in calling twice
# is the same as calling once
class BaseEngine(object):
    __metaclass__ = RegisterEngine
    depends = []

    def __init__(self, **kwargs):
        # We will do this simple resolution here for the
        # time being, so that users don't need the cruft
        # of the entire framework
        if "app_path" not in kwargs or kwargs["app_path"] is None:
            kwargs["app_path"] = default_app_path(__file__, self.__class__.__name__)

        # Given the app path, let's check if it is installed or not
        if(os.path.exists(kwargs["app_path"])): self.installed = True
        else: self.installed = False

        # set it up and delete it
        self.app_path = kwargs["app_path"]; del kwargs["app_path"]

        # give a generic variable setup
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])

    # We will comment this out for the time being, until
    # we can resolve the new system

    #def resolveDepends(self):
    #    __newDepends = dict()
    #    for pack_name in self.__depends__.keys():
    #        package = EngineRegistrar.getPackage(pack_name)
    #        if(isinstance(self.__depends__[pack_name], dict)):
    #            pack = package(copy.deepcopy(self.__depends__[pack_name]))
    #            if not pack.installed: pack.install()
    #            __newDepends[pack_name] = pack.getResolutions(copy.deepcopy(self.__depends__[pack_name]))
    #            for key in __newDepends[pack_name].keys():
    #                ret_val = pack.requestVariable(key)
    #                if ret_val is not None: __newDepends[pack_name][key] = ret_val
    #
    #        elif(isinstance(self.__depends__[pack_name], list)):
    #            __newDepends[pack_name] = list()
    #            for item in self.__depends__[pack_name]:
    #                pack = package(copy.deepcopy(item))
    #                if not pack.installed: pack.install()
    #                __newDepends[pack_name].append(pack.getResolutions(copy.deepcopy(item)))
    #                for key in __newDepends[pack_name][-1].keys():
    #                    ret_val = pack.requestVariable(key)
    #                    if ret_val is not None: __newDepends[pack_name][-1][key] = ret_val
    #    self.__depends__ = __newDepends

    def start(self): raise NotImplemented
    def default_start(self, func_callback):
        if(not self.installed):
            if(not self.install()): return False
        return func_callback()

    def stop(self): raise NotImplemented
    def default_stop(self, func_callback):
        if(not self.installed): return True
        return func_callback()

    def install(self, force = False): raise NotImplemented
    def default_install(self, func_callback, force = False):
        if(force):
            if(not try_delete_path(self.app_path)): raise FilePermissionException
            self.installed = False
        if not os.path.exists(self.app_path):
            os.makedirs(self.app_path)
            self.installed = func_callback()
        return self.installed


    def uninstall(self): raise NotImplemented
    def default_uninstall(self, func_callback = None):
        if(func_callback != None):
            return func_callback()

        if(self.installed == True):
            if(not try_delete_path(self.app_path)):
                raise UninstallingItemDNEException
            self.installed = False


    def restart(self): raise NotImplemented
    def default_restart(self, func_callback = None):
        if(not self.installed):
            if(not self.install()): return False
        if(func_callback == None):
            stop_status = self.stop()
            start_status = self.start()
            return (stop_status and start_status)
        return func_callback()
