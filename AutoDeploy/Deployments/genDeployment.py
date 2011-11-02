from Admin.Admin import getPackage, getPackages, getPackageNames, getEngineFactory
from Utils.Base_Utilities import current_path
from os.path import join
from os import makedirs, getcwd

# This is the Only Item to Be Exported
def genDeployment(packages, rootDirectory = current_path(__file__)):
    if(isinstance(packages, dict)): return __genDictDeployment(packages)
    if(isinstance(packages, list)): return __genListDeployment(packages)
    assert True, "Packages Must Either Be a List or a Dict"


# User Prespecified Routes Taken
def __genDictDeployment(packages, rootDirectory):
    pass


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

def mergeDepends(dep1, dep2):
    # This may seem stupid at first, but
    # it makes handling dependencies easier, since we will put 
    # items at the end which have no dependencies, so 
    # that when we get this list back, we simply need to construct in reverse
    # so dependencies will always be satisfied in linear fashion
    for item in dep2:
        if item in dep1: dep1.remove(item)
        dep1.append(item)
    return dep1

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
    return container