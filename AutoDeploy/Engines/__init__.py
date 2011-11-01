import os, sys
from BaseEngine import EngineRegistrar

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py' or module == "BaseEngine.py":
        continue
    __import__(module[:-3], locals(), globals())

if __name__ == "__main__":
    if(len(sys.argv) != 2 and len(sys.argv) != 3):
        print "\n\tPlease Type the Package Name as First Argument"
        print "\n\tOptionally Second Command can be install, uninstall, start, stop, restart (default is install)"
        print "\n\tHere are the Available Packages to Choose From:\n"
        for key in EngineRegistrar.packages.keys(): print "\t\t%s" % key
        print ""
        sys.exit(0)

    package_name = sys.argv[1]
    if(package_name not in EngineRegistrar.packages):
        print "\n\tSorry that Package '%s' is not available\n" % package_name
        print "\n\tHere are the Available Packages to Choose From:\n"
        for key in EngineRegistrar.packages.keys(): print "\t\t%s" % key
        print ""

    command = "install"
    if(len(sys.argv) == 3): command = sys.argv[2]
    else: command = "install"

    pack = EngineRegistrar.packages[package_name]()

    if command == "install": pack.install()
    elif command == "uninstall": pack.uninstall()
    elif command == "start": pack.start()
    elif command == "stop": pack.stop()
    elif command == "restart": pack.restart()
