from BaseEngine import BaseEngine
from Utils.Base_Utilities import command
from os.path import isdir, join

class Zlib(BaseEngine):
    categories = ["compression"]
    version = "zlib-1.2.5"
    source_url = "http://zlib.net/"

    def install(self, force = False): return self.default_install(self.__zlib_installer, force)

    # Private Methods not to be used Externally
    def __zlib_installer(self):
        command('''curl -o %s.tar.gz "%s%s.tar.gz"''' % (self.version, self.source_url, self.version))
        command('''tar -xzf %s.tar.gz''' % self.version)
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" && make)''' % (self.version, self.app_path))
        command('''rm %s.tar.gz && rm -rf %s''' % (self.version, self.version))
