from CannedZen.Registration import EngineRegistrar, CommandRegistrar, GlobalSettings
from CannedZen.Utils.Base_Utilities import default_app_path, try_delete_path, command
from CannedZen.Utils.FileHelper import FileHelperObject
import os, copy


def getEngineFactory(name):
    try: return EngineRegistrar.classFactories[name]
    except KeyError: return None


# Decorator for Registering an Engine
# This is not really used anywhere, but it means that
# we can register an engine or interact without
# having to use the metaclass inheritance
def registerEngine(cls):
    EngineRegistrar.registerPackage(cls, cls.__name__, cls.categories)

# If we want to register a factory, we'll have to use this method
def registerEngineFactory(func, name):
    EngineRegistrar.classFactories[name] = func

# This is the core metaclass for BaseEngine, it also supports
# command registration as long as class methods are decorated with
# @registerCommand. Then the command is registered with the name of
# the functions name
class RegisterEngine(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(RegisterEngine, cls).__new__
        new_class = super_new(cls, name, bases, attrs)
        if(name != "BaseEngine"):
            registerEngine(new_class)
            methodList = [method for method in dir(new_class) if callable(getattr(new_class, method))]
            registeredMethods = [method for method in methodList if hasattr(getattr(new_class, method), "registerThis")]
            for method in registeredMethods:
                CommandRegistrar.registerCommand(new_class.__name__, getattr(new_class, method), getattr(new_class, method).__name__)
        return new_class

def merge_depends(accum, new_lst):
    new_deps = new_lst
    for item in accum:
        if not item in new_deps: new_deps.append(item)
    return new_deps


def generateDynamicClass(dep):
    # This case to handle on the fly 
    # computed classes needs to be handled better
    # currently it is the case that if there is a
    # parenthesis in the name we consider it dynamic :p
    # for instance PyModule(Django) is a dynamic module
    if("(" in dep and ")" in dep):
        factory, remainder = dep.split("(")
        argument_as_string = remainder.split(")")[0]
        fact = getEngineFactory(factory)
        if(fact is not None):
            return fact(argument_as_string)
    return None


def recurseDepends(basePackage):
    basePackage = str(basePackage)
    container = list()

    # The idea here is if we can't find the 
    # package then we simply assume it is a
    # factory, and if it isn't then we simply
    # print a statement and move on
    pack = getPackage(basePackage)
    if(pack is None):
        pack = generateDynamicClass(basePackage)
        if(pack is None):
            print "Could Not Identify Dependency %s as Package or Factory" % basePackage
            return container

    if(basePackage in container):
        container.remove(basePackage)

    container.append(basePackage)
    for dep in pack.depends:
        rec = recurseDepends(dep)
        #print "Before Merge %s" % container
        container = mergeDepends(container, rec)
        #print "After Merging with %s => %s" % (rec, container)
    return container




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
    depends = []
    optionalArgs = {"app_path" : None}

    def __init__(self, *args, **kw):
        if "global_settings" in kw: self.global_settings = kw["settings"]
        else: self.settings = GlobalSettings()
        
        # Resolve the App Path Issue
        if(self.__class__.__name__ in self.settings.packages):
            if not "app_path" in self.settings.packages[self.__class__.__name__]:
                self.settings.packages[self.__class__.__name__]["app_path"] = self.settings.default_install_path
        else:
            self.settings.packages[self.__class__.__name__] = dict()
            self.settings.packages[self.__class__.__name__]["app_path"] = self.settings.default_install_path
        self.app_path = os.path.join(self.settings.packages[self.__class__.__name__]["app_path"], self.__class__.__name__)

        # Given the app path, let's check if it is installed or not
        if(os.path.exists(self.app_path)): self.installed = True
        else: self.installed = False
        
        self.fileHelper = FileHelperObject(self.__class__.__name__)

    def get_dependencies(self):        
        if(self.depends == []): return [self.__name__]
        
        new_depends = []
        for (depend_name, depend_options) in self.depends:
             new_depends = merge_depends(new_depends, EngineRegistrar.getPackage(depend_name).get_dependencies())
        return new_depends

    def default_start(self, func_callback):
        if(not self.installed):
            if(not self.install()): return False
        return func_callback()

    def stop(self): raise NotImplemented
    def default_stop(self, func_callback):
        if(not self.installed): return True
        return func_callback()

    def resolveDepends(self):
        for pack_name in self.depends:
            package = EngineRegistrar.getPackage(pack_name)
            if(package is None):
                package = generateDynamicClass(pack_name)
                if(package is None):
                    print "Could Not Identify Dependency %s as Package or Factory" % basePackage
                    return

            pack_class = package(settings = self.settings)
            pack_class.install()
            self.settings = pack_class.settings


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


    def restart(self): raise NotImplemented
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