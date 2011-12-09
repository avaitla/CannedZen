class EngineRegistrarObject(object):
    def __init__(self):
        self.categories = {}
        self.packages = {}
        self.engines = {}
    
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
            self.engines[package] = engine()
    
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