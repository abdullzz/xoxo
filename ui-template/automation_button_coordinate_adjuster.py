import sys, os
from lxml import etree

class Core:
    def __init__(self):
        self.path = None
        self.data = None
        self.tree = None
        self.root = None
        self.property = ".//property[contains(@name,'coordinate')]"

    def start(self):
        print(">>>>>> "+sys.argv[0].split(".py")[0]+ " started <<<<<\n")
        if "xoxo.ui" in os.listdir():
            if sys.platform.startswith('win'):
                self.path = str(os.getcwd()) + "\\xoxo"
            else:
                self.path = str(os.getcwd()) + "/xoxo"
            with open(self.path+'.ui','r') as f:
                data = f.read()
            with open(self.path+'.xml', 'w') as f:
                f.write(data)
            with open(self.path+".xml",'r') as f:
                self.data = f.read()
            self.set_tree_and_root()
            self.parseElement()

    def set_tree_and_root(self):
        self.tree = etree.parse(str(os.getcwd()) + "\\xoxo.xml")
        self.root = self.tree.getroot()

    def parseElement(self):
        list = self.root.xpath("count({})".format(self.property))
        if not bool(int(float(list)) == 121):
            print("expected 121 button, got : {}".format(int(float(list))))
        list = self.root.xpath(self.property)

    def printTree(self):
        os.remove(self.path+'.xml')
        # self.tree.write("output.xml")

core = Core()
core.start()
core.printTree()
print("<<<<< ended >>>>>>",end="")