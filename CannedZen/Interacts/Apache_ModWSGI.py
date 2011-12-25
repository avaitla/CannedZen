from CannedZen.BaseInteract import BaseInteract
from CannedZen.Utils.Base_Utilities import command
import os
from CannedZen.Utils import *

class Apache_ModWSGI(BaseInteract):
    engine1name = "Apache"
    engine2name = "ModWSGI"
    
    def install_interaction(self):
        if ("project_path" in self.engine2settings) and ("project_name" in self.engine2settings):
            self.__create_apache_wsgi_conf()
            wsgi_path = os.path.join(self.engine1path, "conf/apache_%s_wsgi.conf" % self.engine2settings["project_name"])
            command('echo "Include \\\"' + wsgi_path + '\\\"" >> ' + str(os.path.join(self.engine1settings["app_path"], "conf/httpd.conf")))
        command("cp %s/.libs/mod_wsgi.so %s/modules/" % (self.engine2settings["app_path"], self.engine1settings["app_path"]))
        print self.engine1settings["app_path"]

    def __create_apache_wsgi_conf(self):
        project_conf = "apache_%s_wsgi.conf" % self.engine2settings["project_name"]
        fh = open(project_conf, "w")
        fh.write('''WSGIScriptAlias / "%s/%s.wsgi"\n\n''' % (self.engine2settings["project_path"], self.engine2settings["project_name"]))
        fh.write('''<Directory "%s">\n''' % os.path.join(self.engine2settings["project_path"], self.engine2settings["project_name"]))
        fh.write('''Allow from all\n''')
        fh.write('''</Directory>''')
        fh.close()
        command("cp %s %s" % (project_conf, os.path.join(self.engine1path, "conf")))