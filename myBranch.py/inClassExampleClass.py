class myColor(object):

    def __init__(self, redChan, greenChan, blueChan, name):
        self.redChan = redChan;
        self.greenChan = greenChan;
        self.blueChan = blueChan;
        self.name = name;

    def description(self):
        print("Hi, I'm a color! My name is {0}." .format(self.name))

smaragdine = myColor(80, 200, 117, "Phil")

#print(smaragdine.redChan)

#print(smaragdine.name)

smaragdine.description()
