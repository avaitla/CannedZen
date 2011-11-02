from CannedZen.BaseEngine import BaseEngine, RegisteredEngine
from CannedZen.Utils.Base_Utilities import command

class Nginx(BaseEngine, RegisteredEngine):
    categories = ["cache", "caching", "server", "proxy", "static"]
    version = "nginx-1.1.4"
    source_url = "http://nginx.org/download/"

    def start(self): return self.default_start(self.__nginx_starter)
    def stop(self): return self.default_stop(self.__nginx_stopper)
    def restart(self): return self.default_restart()
    def install(self, force = False): return self.default_install(self.__nginx_installer, force)
    def uninstall(self): return self.default_uninstall()


    # Private Methods not to be used Externally
    def __nginx_installer(self):
        command('''curl -o "%s.tar.gz" "%s%s.tar.gz"''' % (self.version, self.source_url, self.version))
        command('''tar -xzf "%s.tar.gz"''' % self.version)
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" --without-http_rewrite_module 
                    --without-http_gzip_module && make && make install)''' % (self.version, self.app_path))
        command('''rm -rf %s && rm %s.tar.gz''' % (self.version, self.version))
        return True

    def __nginx_stopper(self): command('''sudo "%s/sbin/nginx -s stop''' % self.app_path)
    def __nginx_starter(self): command('''sudo "%s/sbin/nginx''' % self.app_path)
