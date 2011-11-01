from BaseEngine import BaseEngine
from Utils.Base_Utilities import command
from os.path import join
import os

class Django(BaseEngine):
    categories = ["python", "module", "virtualenv"]
    __depends__  = {"PyModule" : {"module_name" : "django", "app_path" : None, "VirtualEnv" : None}}

    def __init__(self, kwargs = {}):
        try: self.project_name = kwargs["project_name"]
        except KeyError: self.project_name = "DjangoProject"
        super(Django, self).__init__(kwargs)

    def install(self, sudo = False):
        django_admin = join(self.__depends__["PyModule"]["VirtualEnv"], "bin/django-admin.py")
        os.makedirs(self.app_path)
        command("(cd %s && %s startproject %s && mkdir static)" % 
                 (self.app_path, django_admin, self.project_name))
