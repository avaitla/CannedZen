from BaseEngine import BaseEngine
from Utils.Base_Utilities import command

class HAProxy(BaseEngine):
    categories = ["server", "load balancing"]
    version = "haproxy-1.4.18"
    source_url = "http://haproxy.1wt.eu/download/1.4/src/"

    def install(self, force = False): return self.default_install(self.__haproxy_installer, force)
    def uninstall(self): return self.default_uninstall()

    # Private Methods not to be used Externally
    def __haproxy_installer(self):
        command('''curl -o "%s.tar.gz" "%s%s.tar.gz"''' % (self.version, self.source_url, self.version))
        command('''tar -xzf "%s.tar.gz"''' % self.version)
        command('''(cd %s && make TARGET=generic && cp haproxy %s)''' %  (self.version, self.app_path))
        command('''rm -rf %s && rm %s.tar.gz''' % (self.version, self.version))
        return True
