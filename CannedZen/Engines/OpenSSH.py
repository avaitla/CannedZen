from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command
from os.path import isdir, join

class OpenSSH(BaseEngine):
    categories = ["server", "version-control"]
    version = "mod_wsgi-2.5"
    source_url = "http://modwsgi.googlecode.com/files/"
    depends = ["Zlib", "OpenSSL"]

    def install(self, force = False): return self.default_install(self.__ssh_installer, force)

    # Private Methods not to be used Externally
    def __ssh_installer(self):
        command('''curl -o  "%s%s.tar.gz"''' % (self.source_url, self.version))
        command('''tar -xzf ''')
        command('''(cd  && chmod u+x configure && ./configure --prefix="%s" --with-ipv4-default --with-md5-passwords && make)''' % self.app_path)
        command('''rm .tgz && rm -rf ''')
