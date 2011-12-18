from CannedZen import GlobalSettings
from CannedZen.Utils.Print import Printer
from CannedZen.Utils.Base_Utilities import command
import os
import urllib2, tarfile

class FileHelperObject(object):
    def __init__(self, name):
        self.buildDir = os.path.join(GlobalSettings.buildDirectory, name)
    
    def download(self, url, dest):
        destination = os.path.join(GlobalSettings.downloadCache, dest)
        if os.path.exists(destination):
            Printer.printString("Using local copy of %s" % dest)
        else:
            if not os.path.exists(GlobalSettings.downloadCache):
                os.mkdir(GlobalSettings.downloadCache)
            f = open(destination,'wb+')
            Printer.printString("Downloading %s" % (url))
            f.write(urllib2.urlopen(url).read())
            Printer.printString("Finished. File downloaded to %s" % destination)
            f.close()
        if not os.path.exists(self.buildDir):
            os.mkdir(self.buildDir)
        linkFile = os.path.join(self.buildDir, dest)
        if os.path.exists(linkFile):
            os.remove(linkFile)
        os.symlink(destination, linkFile)
        return linkFile
    
    def unTar(self, tarFile):
        
        basename = os.path.basename(tarFile)
        extractPath = self.buildDir
        Printer.printString("Preparing to extract %s" % (tarFile))
        
        tfile = tarfile.open(tarFile)
        
        conf = ""
        #find the configure file
        for fil in tfile.getnames():
            if fil.endswith('configure'):
                conf = fil
        if tarfile.is_tarfile(tarFile):
            tfile.extractall(extractPath)
        else:
            Printer.printString(theTarFile + " is not a tarfile.")
        return os.path.dirname(os.path.join(extractPath, conf))
    
    def cleanUp(self):
        command("rm -rf %s" % self.buildDir)