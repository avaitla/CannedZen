from Admin.Admin import getPackage, getPackages, getPackageNames, get
from Utils.Base_Utilities import current_path

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

<<<<<<< HEAD
def SinglePackage(package_name):
    
=======

def generateDynamicClass(string):
    # This case to handle on the fly 
    # computed classes needs to be handled better
    # currently it is the case taht if there is a
    # parenthesis in the name we consider it dynamic :p
    # for instance PyModule(Django) is a dynamic module
    if("(" in dep and ")" in dep):
        factory, remainder = dep.split("(")
        argument = remainder.split(")")[0]
        


def recurseDepends(basePackage):
    basePackage = str(basePackage)

    container = set()
    pack = getPackage(basePackage)
    container.append(basePackage)
    for dep in pack.depends:

        
        container = container.union(recurseDepends(dep))
    return container
>>>>>>> git commits faulty
