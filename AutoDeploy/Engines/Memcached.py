from BaseEngine import BaseEngine
from Utils.Base_Utilities import command, curry


class Memcached(BaseEngine):
    categories = ["cache", "caching"]
    version = "memcached-1.4.8_rc1"
    source_url = "http://memcached.googlecode.com/files/"
    depends = ["LibEvent"]

    def start(self, ip = "127.0.0.1", port = 11211, mb = 64, user = "$USER"):
        func = curry(self.__memcached_starter)(ip)(port)(mb)(user)
        return default_start(func)

    def stop(self): return self.default_stop(self.__memcached_stopper)
    def restart(self): return self.default_restart(self.__memcached_restarter)
    def install(self, force = False): return self.default_install(self.__memcached_installer, force)
    def uninstall(self): return self.default_uninstall()


    # Private Methods not to be used Externally
    def __memcached_installer(self):
        command('''curl -o "%s.tar.gz" "%s%s.tar.gz"''' % (self.version, self.source_url, self.version))
        command('''tar -xzf "%s.tar.gz"''' % self.version)
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" --with-libevent="%s" && make && make install)''' % 
               (self.version, self.app_path, self.LibEvent))
        command('''rm -rf %s && rm %s.tar.gz''' % (self.version, self.version))
        return True

    def __memcached_stopper(self):
        command('''sudo kill -9 `ps aux | grep memcached | grep -v grep | awk '{print $2}'`''')
        self.address = None
        return True

    def __memcached_starter(self, ip, port, mb, user):
        command('''sudo "%s/bin/memcached" -d -u %s -I %s -p %s -m %s''' % (self.app_path, user, ip, port, mb))
        self.address = "%s:%s/" % (ip, port) 
        return True
