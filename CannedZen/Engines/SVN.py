from BaseEngine import BaseEngine
from Utils.Base_Utilities import command
from os.path import isdir, join

class SVN(BaseEngine):
    categories = ["server", "version-control"]
    version = "subversion-1.6.17"
    source_url = "http://subversion.tigris.org/downloads/"
    depends = ["ApachePortableRuntime"]

    def install(self, force = False): return self.default_install(self.__svn_installer, force)

    # Private Methods not to be used Externally
    def __svn_installer(self):
        command('''curl -o %s.tar.bz2 "%s%s.tar.bz2"''' % (self.version, self.source_url, self.version))
        command('''tar -xjvf %s.tar.bz2''' % (self.version))
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" && make && make install)''' % (self.version, self.app_path))
        command('''rm %s.tar.bz2 && rm -rf %s''' % (self.version, self.version))
