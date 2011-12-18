from CannedZen.Deployments.genDeployment import InteractionDeployment
from CannedZen.Engines import Apache, ModWSGI, Django

class FullDjango(InteractionDeployment):
    engines = [Apache, ModWSGI, Django]
    
FullDjango().install()


from Admin.Admin import generateDeployment

rootDirectory = None
packages1 = ["Apache"   , "VirtualEnv",
            "PostgreSQL", "Django", 
            "Memcached" , "Nginx"]

# We should also be able to custom include
# package specific options, such as install
# paths for which we include the following
# format to generate a deployment
packages2 = {"Apache" : {}, "VirtualEnv" : {},
            "PostgreSQL" : {}, "Django" : {},
            "Memcached" : {}, "Nginx" : {}}

# The second argumnet is optional, and will simply default to wherever
# you are running the script from.
deplyoment = generateDeployment(packages1, rootDirectory)

print deployment.status

# This will check all paths work
deployment.deploy()

print deployment.status

# We can also forcefully overwrite paths with
# deployment.deploy(force = True)

print deployment.info()
print deployment.verbose_info()

apache = deployment.packages["apache"]

print apache.info()
print apache.verbose_info()

apache.uninstall()

# In case Apache has dependencies to Other Systems
# the above may not uninstall apache, but the user may have to do
# apache.uninstall(force = True), however, now the system
# may be out of sync.

print deployment.info()
print deployment.status