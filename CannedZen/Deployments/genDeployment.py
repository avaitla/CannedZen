from CannedZen.Registration import EngineRegistrar, CommandRegistrar, GlobalSettings
from CannedZen.BaseInteract import InteractRegistrar
from CannedZen.Utils.Base_Utilities import current_path
from CannedZen import Interacts
from os.path import join
from itertools import combinations
from os import makedirs, getcwd

def getEngineFactory(name):
    try: return EngineRegistrar.classFactories[name]
    except KeyError: return None

def generateDynamicClass(dep):
    # This case to handle on the fly 
    # computed classes needs to be handled better
    # currently it is the case that if there is a
    # parenthesis in the name we consider it dynamic :p
    # for instance PyModule(Django) is a dynamic module
    if("(" in dep and ")" in dep):
        factory, remainder = dep.split("(")
        argument_as_string = remainder.split(")")[0]
        fact = getEngineFactory(factory)
        if(fact is not None):
            return fact(argument_as_string)
    return None

def merge_depends(accum, new_lst):
    new_deps = new_lst
    for item in accum:
        if not item in new_deps: new_deps.append(item)
    return new_deps
    
def get_dependencies(eng):      
    if(eng.depends == []): return [eng.__name__]
    new_depends = [eng.__name__]
    for depend_name in eng.depends:
         eng = EngineRegistrar.getPackage(depend_name)
         if eng is None:
            eng = generateDynamicClass(depend_name)
            if eng is None:
                print "Could Not Identify Dependency %s as Package or Factory" % basePackage
                return
                
         new_depends = merge_depends(new_depends, eng.depends)
    return new_depends

class InteractionDeployment(object):
    engines = []
    
    def __init__(self, *args, **kwargs):
        if "settings" not in kwargs: self.settings = GlobalSettings()
        else: self.settings = kwargs["settings"]
    
    def install(self):
        for engine in self.engines:
            eng = engine(settings = self.settings)
            eng.install()
            self.settings = eng.settings
        
        total_depends = []
        for item in self.engines: total_depends = merge_depends(total_depends, get_dependencies(item))
        print total_depends
        
        print(self.settings)
        input("Try Interacts?")
        pairs = combinations(total_depends, 2)
        for (pair1, pair2) in pairs:
            print ("Checking: (%s, %s)" % (pair1, pair2))
            interaction = InteractRegistrar.getInteraction(pair1, pair2)
            if(interaction is None): continue
            inst = interaction(self.settings)
            inst.install()
        
                
'''
# All Defaults Are Taken
def __genListDeployment(packages, rootDirectory):
    dependencyHandler = list()
    for pack in packages:
        cls = getPackage(pack)
        depends = cls.__depends__

def install(package, rootdir = None, projectname = "MyProject"):
    if(isinstance(package, str)):
        multiplePackages([package], rootdir = rootdir)
    if(isinstance(package, list)):
        multiplePackageskage(package, projectname = projectname, rootdir)
    assert True, "Argument must either be single string or list of strings, we recieved %s" $ package

def multiplePackages(names, projectname = None, rootdir = None):
    if(rootdir is None): rootdir = getcwd()
    if(projectname is None): package_root = join(rootdir, names[0])
    else: package_root = join(rootdir, projectname)
    depends = list()
    for name in names: depends = mergeDepends(depends, recurseDepends(name))
    __install_helper(depends, package_root)

def __install_helper(depends, package_root):
    print "We need to Satisfy the following Dependencies: %s" % depends
    app_path_settings = dict()
    execution = list()
    for depend in depends[::-1]:
        if(len(depends) == 1): app_path = package_root 
        else: app_path = join(package_root, depend)
        pack = getPackage(depend)(app_path = app_path, **app_path_settings)
        app_path_settings[depend] = pack.app_path
        execution.append(pack)

    print "Setup the Following Paths: %s" % app_path_settings
    for item in execution:
        item.install()
        
def generateDynamicClass(dep):
    # This case to handle on the fly 
    # computed classes needs to be handled better
    # currently it is the case that if there is a
    # parenthesis in the name we consider it dynamic :p
    # for instance PyModule(Django) is a dynamic module
    if("(" in dep and ")" in dep):
        factory, remainder = dep.split("(")
        argument_as_string = remainder.split(")")[0]
        fact = getEngineFactory(factory)
        if(fact is not None):
            return fact(argument_as_string)
    return None


def recurseDepends(basePackage):
    basePackage = str(basePackage)
    container = list()

    # The idea here is if we can't find the 
    # package then we simply assume it is a
    # factory, and if it isn't then we simply
    # print a statement and move on
    pack = getPackage(basePackage)
    if(pack is None):
        pack = generateDynamicClass(basePackage)
        if(pack is None):
            print "Could Not Identify Dependency %s as Package or Factory" % basePackage
            return container

    if(basePackage in container):
        container.remove(basePackage)

    container.append(basePackage)
    for dep in pack.depends:
        rec = recurseDepends(dep)
        #print "Before Merge %s" % container
        container = mergeDepends(container, rec)
        #print "After Merging with %s => %s" % (rec, container)
    return container'''