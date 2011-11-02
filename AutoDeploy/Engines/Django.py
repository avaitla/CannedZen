from BaseEngine import BaseEngine
from Utils.Base_Utilities import command
from os.path import join
import os

class Django(BaseEngine):
    categories = ["python", "module", "virtualenv"]
    depends = ["PyModule(Django)"]

    def __init__(self, **kwargs):
        try: self.project_name = kwargs["project_name"]
        except KeyError: self.project_name = "DjangoProject"
        super(Django, self).__init__(**kwargs)

    def install(self, sudo = False):
        # eventually change virtualenv to pymoduledjango
        # this should not need to know that it has access to a virtualenv
        django_admin = join(self.VirtualEnv, "bin/django-admin.py")
        os.makedirs(self.app_path)
        command("(cd %s && %s startproject %s && mkdir static)" % 
                 (self.app_path, django_admin, self.project_name))
