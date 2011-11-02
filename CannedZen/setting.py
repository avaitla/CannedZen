import os

class SettingsObject(object):
    def __init__(self, installPath = "", virtualEnvPath = "", localPath=""):
        self.executingPath = os.getcwd()
        if installPath:
            self.installPath = installPath 
        else:
            self.installPath = os.path.join(self.executingPath, 'czinstall', 'bin')
        if virtualEnvPath:
            self.virtualEnvPath = virtualEnvPath
        else:
            self.virtualEnvPath = os.path.join(self.executingPath, 'czinstall', 'virtualenv')
        if localPath:
            self.configureLocal(localPath)
        else:
            self.configureLocal(os.path.join(os.getcwd(), 'local'))
            
    def reconfigure(self, *args, **kw):
        for key, value in kw.items():
            setattr(self, key, value)
    
    def configureLocal(self, path):
        self.reconfigure(localPath = path, downloadCache = os.path.join(path, 'cache'), buildDirectory = os.path.join(path, 'build'))

    def getInstallPath(self):
        return self.installPath
    
    def getVirtualEnvPath(self):
        return self.virtualEnvPath
