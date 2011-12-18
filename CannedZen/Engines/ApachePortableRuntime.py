from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command
from os.path import isdir, join

class ApachePortableRuntime(BaseEngine):
    categories = ["apache"]
    version = "apr-1.4.5"
    source_url = "http://apache.opensourceresources.org/apr/"

    def install(self, force = False): return self.default_install(self.__apr_installer, force)

    # Private Methods not to be used Externally
    def __apr_installer(self):
        command('''curl -o %s.tar.gz "%s%s.tar.gz"''' % (self.version, self.source_url, self.version))
        command('''tar -xzf %s.tar.gz''' % (self.version))
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" && make && make install)''' % (self.version, self.app_path))
        command('''rm %s.tar.gz && rm -rf %s''' % (self.version, self.version))
