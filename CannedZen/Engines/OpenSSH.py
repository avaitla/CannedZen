from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command
from os.path import isdir, join

class OpenSSH(BaseEngine):
    categories = ["server", "version-control"]
    version = "openssh-5.9p1"
    source_url = "ftp://ftp3.usa.openbsd.org/pub/OpenBSD/OpenSSH/portable/"
    depends = ["Zlib", "OpenSSL"]

    def install(self, force = False): return self.default_install(self.__ssh_installer, force)

    # Private Methods not to be used Externally
    def __ssh_installer(self):
        command('''wget "%s%s.tar.gz"''' % (self.source_url, self.version))
        command('''tar -xzf %s.tar.gz''' % self.version)
        command('''(cd  && chmod u+x configure && ./configure --prefix="%s" --with-ipv4-default --with-md5-passwords && make)''' % self.app_path)
        command('''rm .tgz && rm -rf ''')
