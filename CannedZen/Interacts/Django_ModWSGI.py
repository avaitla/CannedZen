from CannedZen.BaseInteract import BaseInteract
from CannedZen.Utils.Base_Utilities import command


class Django_ModWSGI(BaseInteract):
    engine1name = "Django"
    engine2name = "ModWSGI"
    
    def install_interaction(self):
        self.__create_django_wsgi_conf()

    # See http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango
    def __create_django_wsgi_conf(self):
        wsgi_conf = self.engine1settings["project_name"] + ".wsgi"
        fh = open(wsgi_conf, "w")
        fh.write("import os, sys\nsys.path.append('%s')\n" % self.engine1settings["app_path"])
        fh.write("os.environ['DJANGO_SETTINGS_MODULE']=%s.settings\n\n" % self.engine1settings["project_name"])
        fh.write("import django.core.handlers.wsgi\n")
        fh.write("application = django.core.handlers.wsgi.WSGIHandler()\n")
        fh.close()
        command("mv %s %s" % (wsgi_conf, self.engine1settings["app_path"]))