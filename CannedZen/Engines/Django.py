from CannedZen.BaseEngine import BaseEngine
from CannedZen.Registration import registerCommand

from CannedZen.Utils.Base_Utilities import command
from os.path import join
import os

class Django(BaseEngine):
    categories = ["python", "module", "virtualenv"]
    description = "Installs the Django web framework."
    depends = ["PyModule(Django)"]

    def __init__(self, *args, **kw):
        try: self.project_name = kw["project_name"]
        except KeyError: self.project_name = "DjangoProject"
        super(Django, self).__init__(*args, **kw)
        
    def install(self, force = False):
        self.default_install(self.newProject, force)
        self.newProject()

    @registerCommand
    def newProject(self, project_name = "NewProject", sudo = False):
        django_admin = join(self.settings.packages["VirtualEnv"]["app_path"], "bin/django-admin.py")
        os.makedirs(self.app_path)
        command("(cd %s && %s startproject %s && mkdir static)" % 
                 (self.app_path, django_admin, project_name))
