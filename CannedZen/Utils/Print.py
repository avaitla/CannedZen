class PrinterObject(object):
    base_level = 8

    def __init__(self):
        self.level = PrinterObject.base_level
        self.decorator = " "
    
    def setLevel(self, level):
        self.level = level
    
    def increaseLevel(self, ammount=4):
        self.level += ammount
    
    def decreaseLevel(self, ammount=4):
        self.level -= ammount
    
    def returnToBase(self, newLineSpace=True):
        self.level = PrinterObject.base_level
        if newLineSpace:
            print "\n\n"
    
    def fixedWidth(self, s1, s2, size, filler = "."):
        blocksize = len(s1)
        fill_needed = size - blocksize
        return "%s %s %s" % (s1, filler*fill_needed, s2)
        
    
    def printString(self, s, prepend=""):
        for line in s.splitlines():
            print "%s%s%s" % (self.decorator*self.level, prepend, line)

Printer = PrinterObject()
    