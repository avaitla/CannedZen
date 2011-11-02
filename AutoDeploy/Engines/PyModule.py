from BaseEngine import BaseEngine
from Utils.Base_Utilities import command
from os.path import join

# In this case, we build the classes on the fly.
# this is essentially a Class Factory.
def PyModule(module_name):
    def install(self, sudo = False):
        self.__pymodule_installer(sudo)
        return True

    # Private Methods not to be used Externally
    def __pymodule_installer(self, sudo = False):
        if self.__depends__["VirtualEnv"]["app_path"] is not None:
            command("%s/bin/pip install %s" % (self.__depends__["VirtualEnv"]["app_path"], self.module_name))
        else:        
            if sudo: command('''sudo pip install %s''' % self.module_name)
            else: command('''pip install %s''' % self.module_name)

    def requestVariable(self, string):
        if(string == "VirtualEnv"): return self.__depends__["VirtualEnv"]["app_path"]

    customClass = type("PyModule(%s)" % str(module_name), (BaseEngine,), {"install" : install, 
                       "__pymodule_installer" : __pymodule_installer,
                       "requestVariable" : requestVariable, "depends" : ["VirtualEnv"], "categories" : ["python", "module", "virtualenv"]})
    return customClass
