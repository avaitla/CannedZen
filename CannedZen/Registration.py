class EngineRegistrarObject(object):
    def __init__(self):
        self.categories = {}
        self.packages = {}
        self.engines = {}
        self.classFactories = {}
    
    def registerPackage(self, engine, name, categories=[]):
        self.packages[name] = engine
        for category in categories:
            self.categories.setdefault(category, []).append(name)
    
    def getPackage(self, name):
        return self.packages.get(name, None)
    
    def packageExists(self, name):
        return self.packages.has_key(name)
    
    def initializeEngines(self):
        for package, engine in self.packages.items():
            self.engines[package] = engine
            
class InteractsRegistrarObject(object):
    def __init__(self):
        self.custom_pairs = dict()

    # For the Time Being We will only permit one interaction
    # type between two deployment engines, we may remove this restriction later
    def registerInteract(self, interaction, engine1_as_str, engine2_as_str):
        # Just in case a User sends in the actual engine object
        # We will try our best to cast them into Strings
        engine1_as_str = str(engine1_as_str)
        engine2_as_str = str(engine2_as_str)

        assert (engine1_as_str, engine2_as_str) not in self.custom_pairs, "Interaction between Engines %s and %s Exists" % (engine1_as_str, engine2_as_str)
        self.custom_pairs[(engine1_as_str, engine2_as_str)] = self.custom_pairs[(engine1_as_str, engine2_as_str)] = interaction

    def getInteraction(self, engine1_as_str, engine2_as_str):
        engine1_as_str = str(engine1_as_str)
        engine2_as_str = str(engine2_as_str)

        return self.custom_pairs.get((engine1_as_str, engine2_as_str), None)


class GlobalSettings(dict):
    packages = {}
    default_install_path = "/Users/Tigger/Apache"


















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
    
    
class OptionRegistrarObject(object):
    def __init__(self):
        self.options = {}
        self.i = 2
    
    def __getitem__(self, item):
        return self.i

class CommandRegistrarObject(object):
    def __init__(self):
        self.enginecommands = {}
    
    def registerCommand(self, engine, command, name):
        self.enginecommands[engine] = self.enginecommands.get(engine, {})
        self.enginecommands[engine][name] = command
        
    
    def __getitem__(self, item):
        return self.i

class registerClassToCommand(object):
    def __init__(self, c):
        self.c = c
    
    def __call__(self, f, *args, **kw):
        CommandRegistrar.registerCommand(self.c, f.f, f.f.__name__)
        return f


class registerEngine(object):
    def __init__(self, e):
        self.e = e
        
    
    def __call__(self, *args, **kw):
        self.e(*args, **kw)

def registerCommand(func):
    func.registerThis = True
    return func

CommandRegistrar = CommandRegistrarObject()
EngineRegistrar = EngineRegistrarObject()
InteractRegistrar = InteractsRegistrarObject()