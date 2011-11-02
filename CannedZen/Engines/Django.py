from CannedZen.BaseEngine import BaseEngine, RegisteredEngine
import PyModule
from CannedZen.Registration import registerCommand

from CannedZen.Utils.Base_Utilities import command
from os.path import join
import os

class Django(BaseEngine, RegisteredEngine):
    categories = ["python", "module", "virtualenv"]
    description = "Installs the Django web framework."
    __depends__  = {"PyModule" : {"module_name" : "django", "app_path" : None, "VirtualEnv" : None}}

    def __init__(self, *args, **kw):
        
        try: self.project_name = kw["project_name"]
        except KeyError: self.project_name = "DjangoProject"
        super(Django, self).__init__(*args, **kw)
        

    @registerCommand
    def newProject(self, sudo = False):
        django_admin = join(self.__depends__["PyModule"]["VirtualEnv"], "bin/django-admin.py")
        os.makedirs(self.app_path)
        command("(cd %s && %s startproject %s && mkdir static)" % 
                 (self.app_path, django_admin, self.project_name))
