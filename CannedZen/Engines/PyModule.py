from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command
from os.path import join

class PyModule(BaseEngine):
    categories = ["python", "module", "virtualenv"]
    __depends__ = {"VirtualEnv" : {}, "Python": {}}
    
    def __init__(self, *args, **kw):
        super(PyModule, self).__init__(*args, **kw)
        
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
