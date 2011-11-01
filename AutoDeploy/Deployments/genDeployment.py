from Admin.Admin import getPackage, getPackages, getPackageNames
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
