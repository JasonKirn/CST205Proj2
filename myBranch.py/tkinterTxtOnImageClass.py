import tkinter
from tkinter import *
#from tkinter.fileddialog import askopenfilename#prob don't need for this
from PIL import Image, ImageTk

class uiFrame(Frame):
    def mouse_click(self,event):
        if(self.pixelWidth is None):
            app.canvas.create_rectangle(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="blue")
            self.click_points[self.click_count] = (event.x, event.y)
            if(self.click_count%2==1):
                self.draw_line()
                self.click_count = 0
                return
            self.click_count = self.click_count + 1

    def draw_line(self):
        x1 = self.click_points[self.click_count - 1][0]
        y1 = self.click_points[self.click_count - 1][1]
        x2 = self.click_points[self.click_count][0]
        y2 = self.click_points[self.click_count][1]
        app.canvas.create_line(x1, y1, x2, y2)

    def __init__(self,parent):
        Frame.__init__(self,parent,background="gray")
        """
        Declaring instance variables:
        Some of these lines are technically redundant
        But its good to have a list of your class's instance variables
        in one easy locate place as opposed to simply
        declaring and assigning them when you use them.
        """
        self.parent = parent
        self.canvas = Canvas(self, width=800, height=500)
        self.click_points = {}
        self.click_count = 0
        self.finddistance_button = None
        self.calibrationfile_button = None
        self.calibrationimage_button = None
        self.programLabel = None
        self.Label = None
        self.Button = None
        self.calibration_filename = ""
        self.image_filename = ""
        self.image = None
        self.processed_image = None

        self.pixelWidth = None
        self.FOV = 0.0

        self.init_ui()


    def init_ui(self):
        #self.Label(root, image=tkimage, text = "Hackerman was here", fg = "orange", font = ("Helvetica", 20), compound = tkinter.CENTER).pack(side = tkinter.BOTTOM, anchor = tkinter.S)
        self.calibrationfile_button = Button(text = "Set Ult to 100%").pack(side= tkinter.TOP, anchor= tkinter.N, expand= tkinter.YES)
        self.programLabel = Label(text="Some info: Don't report pls").pack(side = tkinter.LEFT, anchor = tkinter.N)
        self.programLabel = Label(text="Enter account info for free hacks:").pack(side = tkinter.TOP, anchor = tkinter.N)
        self.calibrationfile_button = Button(text = "Quit", command = root.quit).pack(side = tkinter.BOTTOM, anchor = tkinter.W)
        #self.calibrationfile_button = Button(text = "Enter", command = show_entry_fields).pack(side = tkinter.BOTTOM, anchor = tkinter.S)

if __name__ == '__main__':
    root = Tk()
    app = uiFrame(root)
    root.mainloop()
