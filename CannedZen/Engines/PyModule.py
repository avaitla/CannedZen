from CannedZen.BaseEngine import BaseEngine, registerEngineFactory
from CannedZen.Utils.Base_Utilities import command
from os.path import join

# In this case, we build the classes on the fly.
# this is essentially a Class Factory.
def PyModule(module_name):
    def __init__(self, **kwargs):
        BaseEngine.__init__(self, **kwargs)
        self.app_path = self.settings.packages["VirtualEnv"].get("app_path", None)
        
    def install(self, sudo = False):
        self.__pymodule_installer(sudo)
        return True

    # Private Methods not to be used Externally
    def __pymodule_installer(self, sudo = False):
        if self.settings.packages["VirtualEnv"]["app_path"] is not None:
            command("%s/bin/pip install %s" % (self.settings.packages["VirtualEnv"]["app_path"], self.module_name))
        else:        
            if sudo: command('''sudo pip install %s''' % self.module_name)
            else: command('''pip install %s''' % self.module_name)

    def requestVariable(self, string):
        if(string == "VirtualEnv"): return self.settings.packages["VirtualEnv"]["app_path"]

    customClass = type("PyModule(%s)" % str(module_name), (BaseEngine,), {"__init__" : __init__, "install" : install, 
                       "__pymodule_installer" : __pymodule_installer, "module_name" : module_name,
                       "requestVariable" : requestVariable, "depends" : ["VirtualEnv"], "categories" : ["python", "module", "virtualenv"]})
    return customClass

# Eventually we'll make this a decorator
registerEngineFactory(PyModule, "PyModule")