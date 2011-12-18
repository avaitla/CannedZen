from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command
from os.path import isdir, join

class Git(BaseEngine):
    categories = ["server", "version-control"]
    version = "git-1.7.7.1"
    source_url = "http://git-core.googlecode.com/files/"

    def install(self, force = False): return self.default_install(self.__git_installer, force)

    # Private Methods not to be used Externally
    def __git_installer(self):
        command('''curl -o git-1.7.7.1.tar.gz "%s%s.tar.gz"''' % (self.source_url, self.version))
        command('''tar -xzf git-1.7.7.1.tar.gz''')
        command('''(cd git-1.7.7.1 && chmod u+x configure && ./configure --prefix="%s" && make && make install)''' % self.app_path)
        command('''rm git-1.7.7.1.tar.gz && rm -rf git-1.7.7.1''')
