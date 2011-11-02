from CannedZen.Registration import EngineRegistrar, CommandRegistrar
from CannedZen.Utils.Base_Utilities import default_app_path, try_delete_path, command
from CannedZen.Utils.FileHelper import FileHelperObject
from CannedZen import GlobalSettings
import os, copy

# Decorator for Registering an Engine
# This is not really used anywhere, but it means that
# we can register an engine or interact without
# having to use the metaclass inheritance
def registerEngine(cls):
    EngineRegistrar.registerPackage(cls, cls.__name__, cls.categories)


class RegisterEngine(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(RegisterEngine, cls).__new__
        new_class = super_new(cls, name, bases, attrs)
        if(name != "BaseEngine"):
            EngineRegistrar.registerPackage(new_class, new_class.__name__, new_class.categories)
            methodList = [method for method in dir(new_class) if callable(getattr(new_class, method))]
            registeredMethods = [method for method in methodList if hasattr(getattr(new_class, method), "registerThis")]
            for method in registeredMethods:
                CommandRegistrar.registerCommand(new_class.__name__, getattr(new_class, method), getattr(new_class, method).__name__)
        return new_class

# This is the Base Class for a Plug and Play Component
# The functions listed are mostly left as interface methods
# which should be reimplemented by items inherting this
# base class. It should not be used unless inherited
# All internal methods must be idempotent, as in calling twice
# is the same as calling once
class BaseEngine(object):
    version = "0.0.--.0.0"
    description = "Unimplemented description field."
    __metaclass__ = RegisterEngine
    __depends__ = {}
    __exposes__ = {}

    def __init__(self, *args, **kw):
        kwargs = kw.get('kwargs', {})
        
        if "app_path" not in kwargs or kwargs["app_path"] is None:
            kwargs["app_path"] = os.path.join(GlobalSettings.installPath, self.__class__.__name__)    

        if(os.path.exists(kwargs["app_path"])): self.installed = True
        else: self.installed = False

        self.app_path = kwargs["app_path"]
        del kwargs["app_path"]

        for key in kwargs.keys(): self.__setattr__(key, kwargs[key])
        
        self.fileHelper = FileHelperObject(self.__class__.__name__)

    def resolveDepends(self):
        __newDepends = dict()
        for pack_name in self.__depends__.keys():
            package = EngineRegistrar.getPackage(pack_name)
            if(isinstance(self.__depends__[pack_name], dict)):
                pack = package(copy.deepcopy(self.__depends__[pack_name]))
                if not pack.installed: pack.install()
                __newDepends[pack_name] = pack.getResolutions(copy.deepcopy(self.__depends__[pack_name]))
                for key in __newDepends[pack_name].keys():
                    ret_val = pack.requestVariable(key)
                    if ret_val is not None: __newDepends[pack_name][key] = ret_val

            elif(isinstance(self.__depends__[pack_name], list)):
                __newDepends[pack_name] = list()
                for item in self.__depends__[pack_name]:
                    pack = package(copy.deepcopy(item))
                    if not pack.installed: pack.install()
                    __newDepends[pack_name].append(pack.getResolutions(copy.deepcopy(item)))
                    for key in __newDepends[pack_name][-1].keys():
                        ret_val = pack.requestVariable(key)
                        if ret_val is not None: __newDepends[pack_name][-1][key] = ret_val

        self.__depends__ = __newDepends

    def requestVariable(self, string): return None
    def getResolutions(self, requirements_as_dict):
        for key in requirements_as_dict.keys():
            requirements_as_dict[key] = self.__getattribute__(key)
        return requirements_as_dict


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
        self.resolveDepends()
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

    def restart(self):
        raise NotImplemented

    def default_restart(self, func_callback = None):
        if(not self.installed):
            if(not self.install()): return False
        if(func_callback == None):
            stop_status = self.stop()
            start_status = self.start()
            return (stop_status and start_status)
        return func_callback()
    
    def download(self, *args, **kw):
        return self.fileHelper.download(*args, **kw)
    
    def unTar(self, *args, **kw):
        return self.fileHelper.unTar(*args, **kw)
    
    def runConfigAndMake(self, directory, flags={}):
        
        configPath = os.path.abspath(os.path.join(directory, 'configure'))
        assert os.path.exists(configPath)
        command('chmod u+x %s' % configPath)
        flagString = ''
        for flag, arg in flags.items():
            flagString += flag
            if arg:
                flagString += "=%s" % arg
            flagString += " "
        command('cd %s && bash %s -q %s && make && make install' % (directory, configPath, flagString))
    
    
    def cleanUp(self):
        return self.fileHelper.cleanUp()
