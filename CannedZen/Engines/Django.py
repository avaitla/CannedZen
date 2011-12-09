from CannedZen.BaseEngine import BaseEngine
import PyModule
from CannedZen.Registration import registerCommand

from CannedZen.Utils.Base_Utilities import command
from os.path import join
import os

class Django(BaseEngine):
    categories = ["python", "module", "virtualenv"]
<<<<<<< HEAD
    depends = ["PyModule(Django)"]

    def __init__(self, **kwargs):
        try: self.project_name = kwargs["project_name"]
        except KeyError: self.project_name = "DjangoProject"
        super(Django, self).__init__(**kwargs)

    def install(self, sudo = False):
        # eventually change virtualenv to pymoduledjango
        # this should not need to know that it has access to a virtualenv
        django_admin = join(self.VirtualEnv, "bin/django-admin.py")
=======
    description = "Installs the Django web framework."
    __depends__  = {"PyModule" : {"module_name" : "django", "app_path" : None, "VirtualEnv" : None}}

    def __init__(self, *args, **kw):
        
        try: self.project_name = kw["project_name"]
        except KeyError: self.project_name = "DjangoProject"
        super(Django, self).__init__(*args, **kw)
        

    @registerCommand
    def newProject(self, sudo = False):
        django_admin = join(self.__depends__["PyModule"]["VirtualEnv"], "bin/django-admin.py")
>>>>>>> remotes/dracule/master
        os.makedirs(self.app_path)
        command("(cd %s && %s startproject %s && mkdir static)" % 
                 (self.app_path, django_admin, self.project_name))
