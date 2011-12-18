from CannedZen.BaseEngine import BaseEngine
from CannedZen.Utils.Base_Utilities import command

class VirtualEnv(BaseEngine):
    categories = ["python", "module", "virtualenv"]

    def install(self): self.__virtualenv_installer()

    # Private Methods not to be used Externally
    def __virtualenv_installer(self):
        try: import virtualenv
        except ImportError:
            command('''sudo pip install virtualenv''')
        print self.app_path
        command("virtualenv --no-site-packages %s" % self.app_path)
