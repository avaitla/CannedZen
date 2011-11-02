from CannedZen.Registration import EngineRegistrar, CommandRegistrar
from CannedZen import Engines
import glob, imp
import os
 
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



        