from CannedZen.Registration import EngineRegistrar, CommandRegistrar, InteractRegistrar
from CannedZen import Engines
import glob, imp, os
 
def importPluginModulesIn(dir):
    for path in glob.glob(os.path.join(dir,'[!_]*.py')):
        name, ext = os.path.splitext(os.path.basename(path))
        __import__('Engines', globals(), locals(), [name], -1)

#importPluginModulesIn(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Engines'))
    

def getPackage(name):
    return EngineRegistrar.getPackage(name)

def packageExists(name):
    return EngineRegistrar.packageExists(name)

def getPackages():
    return EngineRegistrar.packages

def getPackageNames():
    return EngineRegistrar.packages.keys()

def getCommands():
    return CommandRegistrar.enginecommands

def getEngine(name):
    return EngineRegistrar.engines.get(name)
    
#from Engines import EngineRegistrar
#from Interacts import InteractRgistrar
#from Deployments import genDeployment

def getEngineFactory(name):
    try: return EngineRegistrar.classFactories[name]
    except KeyError: return None

#def getPackage(name):
#    return EngineRegistrar.getPackage(name)

#def getPackages():
#    return EngineRegistrar.packages

#def getPackageNames():
#    return EngineRegistrar.packages.keys()

#Not working for some reason
#def getInteract(pack1name, pack2name):
#    return InteractRegistrar.getInteraction(pack1name, pack2name)

#def getInteracts():
#    return InteractRegistrar.custom_pairs

#def getInteractNames():
#    return InteractRegistrar.custom_pairs.keys()

#def generateDeployment(packages):
#    return genDeployment(packages)