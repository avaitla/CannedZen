from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command

class Apache(BaseEngine):
    categories = ["server"]
    version = "httpd-2.2.19" 
    source_url = "http://archive.apache.org/dist/httpd/"

    def start(self): return self.default_start(self.__apache_starter)
    def stop(self): return self.default_stop(self.__apache_stopper)
    def restart(self): return self.default_restart(self.__apache_restarter)
    def install(self, force = False): return self.default_install(self.__apache_installer, force)
    def uninstall(self): return self.default_uninstall()


    # Private Methods not to be used Externally
    def __apache_installer(self):
        command('''curl -o "%s.tar.gz" "%s%s.tar.gz"''' % (self.version, self.source_url, self.version))
        command('''tar -xzf "%s.tar.gz"''' % self.version)
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" --enable-mods-shared="all" --enable-deflate --enable-proxy --enable-proxy-balancer --enable-proxy-http && make && make install)''' % (self.version, self.app_path))
        command('''rm -rf %s && rm %s.tar.gz''' % (self.version, self.version))
    def __apache_stopper(self): command('''sudo "%s/bin/apachectl" stop''' % self.app_path)
    def __apache_starter(self): command('''sudo "%s/bin/apachectl" start''' % self.app_path)
    def __apache_restarter(self): command('''sudo "%s/bin/apachectl" restart''' % self.app_path)
