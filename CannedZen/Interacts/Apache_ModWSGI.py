from CannedZen.BaseInteract import BaseInteract
from CannedZen.Utils.Base_Utilities import command


class Apache_ModWSGI(BaseInteract):
    engine1name = "Apache"
    engine2name = "ModWSGI"
    
    def install_interaction(self):
        self.__create_apache_wsgi_conf()
        ret_string = quickTemplateStr(open(os.path.join(current_path(__file__), "Templates/Server_Engine/httpd.conf")).read(),
                     {"WSGI_PATH" : os.path.join(self.django_path, "apache/apache_%s_wsgi.conf" % self.django_project_name)})
        open(os.path.join(self.standard_deployment.server.app_path, "conf/httpd.conf"), "w").write(ret_string)


    def __create_apache_wsgi_conf(self):
        fh = open("apache_%s_wsgi.conf" % self.django_project_name, "w")
        fh.write('''WSGIScriptAlias / "%s/%s.wsgi"\n\n''' % (os.path.join(self.django_path, "apache"), self.django_project_name))
        fh.write('''<Directory "%s">\n''' % os.path.join(self.django_path, "apache"))
        fh.write('''Allow from all\n''')
        fh.write('''</Directory>''')
        fh.close()