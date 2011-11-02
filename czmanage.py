from CannedZen import Admin, GlobalSettings
from CannedZen.Utils.PostionalOptionParser import PosOptionParser
from CannedZen.Utils.Print import Printer
ps = Printer.printString
fw = Printer.fixedWidth
from os.path import join, basename, splitext, abspath, dirname, exists
from os import mkdir, getcwd
from optparse import Option
import sys
import shelve

sys.path.append(abspath(join(getcwd(), 'CannedZen')))
SETTINGS_DB = join(getcwd(), 'local', 'cz.db')


def get_db(filename = SETTINGS_DB):
  if not exists(filename):
    mkdir(dirname(filename))
  return shelve.open(filename)

def list_callback(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))


if '__main__' == __name__:
    cannedzen_db = get_db()
    parser = PosOptionParser("usage: %prog [options] command")
    parser.add_option('-i', '--install',
                  type='string',
                  action='callback',
                  callback=list_callback,
                  dest = 'install',
                  help="A comma seperated list of packages you wish to install")
    
    parser.add_option('--deployment',
                  type='string',
                  action='callback',
                  callback=list_callback,
                  dest = 'deployment',
                  help="A comma seperated list of deployments you wish to install")
       
    parser.add_option('-s', '--search',
                  type='string',
                  action='store',
                  dest = 'searchstring',
                  help = 'Argument to search for a package name')
    
    parser.add_option('-d', '--installDirectory',
                  type='string',
                  action='store',
                  dest = 'installDirectory',
                  help = 'Set the installation directory.')
    
    parser.add_option('-v', '--virtualEnvDir',
                  type='string',
                  action='store',
                  dest = 'virtualEnvDirectory',
                  help = 'Set the directory of the virtual env.')

    parser.add_option('-o', '--outputdir',
                  type='string',
                  action='store',
                  dest = 'outputdir',
                  default = 'installedpackages/',
                  help = "The directory where things will be installed")
    
    parser.add_positional_argument(Option('--command', action='store_true',
                                   help='The bar positional argument'))
    
    (options, args) = parser.parse_args(sys.argv[1:])
    for flag, val in options.__dict__.items():
        if flag == "installDirectory" and val:
          GlobalSettings.reconfigure(installPath = val)
        if flag == 'virtualEnvDirectory' and val:
          GlobalSettings.reconfigure(virtualEnvPath = val)
    ps("\n############################################")
    ps("#                                          #")
    ps("#    Welcome to CannedZen Stack Manager    #")
    ps("#                                          #")
    ps("############################################")
    ps("\nYour install Path is %s" % GlobalSettings.getInstallPath())
    ps("Your virtualenv Path is %s\n" % GlobalSettings.getVirtualEnvPath())
    if options:
      for flag, val in options.__dict__.items():
        if flag == 'searchstring' and val:
          ps("\nSearching for : %s" % val)
          ps("----------------------------")
          found = False
          for package, packageClass in Admin.getPackages().items():
            if val in package:
              Printer.increaseLevel()
              ps(fw("%s (%s)" % (package, packageClass.version), packageClass.toolkit_usage, 40))
              found = True
          if not found:
            Printer.returnToBase()
            ps("No Packages Found", "  ")
        if flag == 'install' and val:
          installing = set() #container for the packages that need to be installed
          dependencies = {}
          
          ps("\nPreparing to install %s" % ', '.join(val))
          ps("----------------------------")
          Printer.increaseLevel()
          for package in val:
            if Admin.packageExists(package):
              packageClass = Admin.getPackage(package)
              ps(fw("%s (%s)" % (package, packageClass.version), packageClass.description, 40))
              installing.add(package)
            else:
              ps("\n!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!")
              ps("Unable to locate package %s! This package will not be installed." % package)
              ps("!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!\n")
          Printer.returnToBase()
          ps("\nChecking Dependencies")
          ps("----------------------------")
          Printer.increaseLevel()
          for package in installing:
              packageClass = Admin.getPackage(package)
              ps(fw("%s (%s)" % (package, packageClass.version), packageClass.description, 40))
              dependencies.update(packageClass.__depends__)
          ps(str(dependencies))
          for package in installing:
            engine = Admin.getEngine(package)
            engine.install(True)
          
          Printer.returnToBase()
          ps("\n\n")
          
    if args:
        if "list_packages" in args:
            ps("\nCurrently Available Packages")
            ps("----------------------------")
            Printer.increaseLevel()
            for package, packageClass in Admin.getPackages().items():
                ps(fw("%s (%s)" % (package, packageClass.version), packageClass.description, 40))
            Printer.returnToBase()
            ps("\n\n")
        if "list_commands" in args:
            ps("\nCurrently Available Commands")
            ps("----------------------------")
            Printer.increaseLevel(8)
            for name, command in Admin.getCommands().items():
                ps("> %s " % (name))
                Printer.increaseLevel(2)
                for com, func in command.items():
                  ps(fw("* %s" % com, "%s" % (func.__doc__), 15, '-'))
                Printer.decreaseLevel(2)
                ps('\n')
            Printer.returnToBase()