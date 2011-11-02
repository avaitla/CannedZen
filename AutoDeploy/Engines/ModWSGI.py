from BaseEngine import BaseEngine
from Utils.Base_Utilities import command
from os.path import isdir, join

class ModWSGI(BaseEngine):
    categories = ["apache", "python"]
    version = "mod_wsgi-2.5" 
    source_url = "http://modwsgi.googlecode.com/files/"
    depends = ["Apache"]

    def install(self, force = False): return self.default_install(self.__modwsgi_installer, force)

    # Private Methods not to be used Externally
    def __modwsgi_installer(self):
        command('''curl -o mod_wsgi.tgz "%s%s.tar.gz"''' % (self.source_url, self.version))
        command('''tar -xzf mod_wsgi.tgz''')
        command('''(cd mod_wsgi-2.5 && chmod u+x configure && ./configure --with-apxs="%s" && make)''' % join(self.app_path, "bin/apxs"))
        command('''rm mod_wsgi.tgz && rm -rf mod_wsgi-2.5''')
