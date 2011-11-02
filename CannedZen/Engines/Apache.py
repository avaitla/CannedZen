from CannedZen.BaseEngine import BaseEngine
from CannedZen.Registration import registerCommand
from CannedZen.Utils.Base_Utilities import command

class Apache(BaseEngine):
    categories = ["server"]
    version = "httpd-2.2.19"
    description = "Installs the Apache Server."
    source_url = "http://archive.apache.org/dist/httpd/"
    
    
    @registerCommand
    def start(self):
        """Starts the Apache server"""
        return self.default_start(self.__apache_starter)
    
    @registerCommand
    def stop(self):
        """Stops the Apache server"""
        return self.default_stop(self.__apache_stopper)
        
    @registerCommand
    def restart(self):
        """Restarts the Apache server"""
        return self.default_restart(self.__apache_restarter)
    def install(self, force = False):
        return self.default_install(self.__apache_installer, force)
    def uninstall(self): return self.default_uninstall()


    # Private Methods not to be used Externally
    def __apache_installer(self):
        tarFile = self.download('%s%s.tar.gz' % (self.source_url, self.version), "%s.tar.gz" % self.version)
        extractedDir = self.unTar(tarFile)
        self.runConfigAndMake(extractedDir, {"--prefix":"%s" % self.app_path,
                                      "--enable-mods-shared":"all",
                                      "--enable-deflate": None,
                                      "--enable-proxy": None,
                                      "--enable-proxy-balancer": None,
                                      "--enable-proxy-http": None})
        #self.makeInstall(extractedDir)
        self.cleanUp()

    def __apache_stopper(self): command('''sudo "%s/bin/apachectl" stop''' % self.app_path)
    def __apache_starter(self): command('''sudo "%s/bin/apachectl" start''' % self.app_path)
    def __apache_restarter(self): command('''sudo "%s/bin/apachectl" restart''' % self.app_path)
