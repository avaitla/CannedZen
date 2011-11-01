from BaseEngine import BaseEngine
from Utils.Base_Utilities import command

class LibEvent(BaseEngine):
    categories = ["event", "notification"]
    version = "libevent-2.0.14-stable"
    source_url = "https://github.com/downloads/libevent/libevent/"

    def __init__(self, kwargs = {}): super(LibEvent, self).__init__(kwargs)

    def install(self, force = False): return self.default_install(self.__libevent_installer, force)

    # Private Methods not to be used Externally
    def __libevent_installer(self):
        command('''wget --no-check-certificate %s%s.tar.gz''' % (self.source_url, self.version))
        command('''tar -xzf %s.tar.gz''' % self.version)
        command('''(cd %s && chmod u+x configure && ./configure --prefix="%s" && make && make install)''' % (self.version, self.app_path))
        command('''rm %s.tar.gz && rm -rf %s''' % (self.version, self.version))
