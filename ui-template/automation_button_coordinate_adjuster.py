import sys, os
from lxml import etree

class Core:
    def __init__(self):
        self.path = None
        self.data = None
        self.tree = None
        self.root = None
        self.property = ".//property[contains(@name,'coordinate')]"
        self.item = ".//item[@row]"

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
        lists = self.root.xpath(self.item)
        for x in lists:
            expected_row = str(int(x.get('row')))
            expected_column = str(int(x.get('column')))
            coordinate = x.xpath(self.property)[0].xpath('.//string')[0]
            actual_row = coordinate
            actual_column = coordinate
            print("Expected Coordinate : {}.{} || Got : {}.{}".format(
                expected_column,
                expected_row,
                str(actual_column.text.split('.')[0]),
                str(actual_row.text.split('.')[1])
            ))
            coordinate.text = "{}.{}".format(expected_column, expected_row)

    def printTree(self):
        os.remove(self.path+'.xml')
        self.tree.write("xoxo.xml")

    def embedXMLEncoding(self):
        with open(self.path+'.xml','r') as f:
            data = f.read()
        with open(self.path+'.ui', 'w') as f:
            header = '<?xml version="1.0" encoding="UTF-8"?>\n'
            f.write(header+data+"\n")
        os.remove(self.path+'.xml')

core = Core()
core.start()
core.printTree()
core.embedXMLEncoding()
print("<<<<< ended >>>>>>",end="")