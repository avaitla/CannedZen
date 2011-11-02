from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command

class Python(BaseEngine):
    categories = ["python"]
    version = "2.7.2"
    source_url = "http://www.python.org/download/releases/"

    def install(self, force = False): return self.default_install(self.__python_installer, force)

    # Private Methods not meant to be used externally
    def __python_installer(self):
        command('''wget %s%s.tar.gz''' % (self.__source_url, self.__version))
        command('''tar -xzf %s.tar.gz''' % self.__version)
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" && make && make install)''' % (self.__version, self.app_path))
        command('''rm %s.tar.gz && rm -rf %s''' % (self.__version, self.__version))
