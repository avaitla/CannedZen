from BaseEngine import BaseEngine
from Utils.Base_Utilities import command
from os.path import isdir, join

class OpenSSL(BaseEngine):
    categories = ["security", "encryption", "ssl", "tls"]
    version = "openssl-1.0.0e"
    source_url = "http://www.openssl.org/source/"

    def install(self, force = False): return self.default_install(self.__openssl_installer, force)

    # Private Methods not to be used Externally
    def __openssl_installer(self):
        command('''curl -o %s.tar.gz "%s%s.tar.gz"''' % (self.version, self.source_url, self.version))
        command('''tar -xzf %s.tar.gz''' % self.version)
        command('''(cd %s && chmod u+x config && ./config --prefix="%s" && make)''' % (self.version, self.app_path))
        command('''rm %s.tar.gz && rm -rf %s''' % (self.version, self.version))
