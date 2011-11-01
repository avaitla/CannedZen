from BaseEngine import BaseEngine
from Utils.Base_Utilities import command

class Bind(BaseEngine):
    categories = ["dns"]
    version = "9.8.0-P4"
    source_url = "ftp://ftp.isc.org/isc/bind/"
    __root_cache = "ftp://ftp.rs.internic.net/domain/db.cache"

    def start(self): return self.default_start(self.__bind_starter)
    def stop(self): return self.default_stop(self.__bind_stopper)
    def restart(self): return self.default_restart(self.__bind_restarter)
    def install(self, force = False): return self.default_install(self.__bind_installer, force)
    def uninstall(self): return self.default_uninstall()


    # Private Methods not to be used Externally
    def __bind_installer(self):
        bind_path = "bind-" + self.version

        command('''curl -o "%s.tar.gz" "%s%s/%s.tar.gz"''' % (bind_path, self.source_url, self.version, bind_path))
        command('''tar -xzf "%s.tar.gz"''' % bind_path)
        command('''(cd "%s" && chmod u+x configure && ./configure --prefix="%s")''' % (bind_path, self.app_path))

        # Without this command, it doesn't seem to build on macs for some reason
        command('''echo "#define __APPLE_USE_RFC_3542" > temp''')
        command('''cat "%s/lib/isc/unix/include/isc/net.h" >> temp''' % bind_path)
        command('''mv temp "%s/lib/isc/unix/include/isc/net.h"''' % bind_path)
        command('''(cd "%s" && make && make install)''' % bind_path)
        command('''rm "%s.tar.gz" && rm -rf "%s"''' % (bind_path, bind_path))
        command('''(cd "%s/etc" && touch named.conf && touch managed-keys.bind)''' % bind_path)
        command('''(cd "%s/var" && mkdir named && cd named && curl %s --user ftp:ftp -O)''' % (bind_path, self.__root_cache))
        command('''(cd "%s" && sbin/rndc-confgen > etc/rndc.conf)''' % bind_path)
        return True

    def __bind_stopper(self): command('''sudo kill -9 `ps aux | grep named | grep -v grep | awk '{print $2}'`''')
    def __bind_starter(self): command('''sudo "%s/sbin/named" -c "%s/etc/named.conf"''' % self.app_path)
