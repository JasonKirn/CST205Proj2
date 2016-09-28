from tkinter import *
from PIL import Image, ImageTk

class DistanceFinderFrame(Frame):

    def mouse_click(self,event):
        app.canvas.create_recetangle(even.x - 5, event.y - 5, event.x + 5, event.y + 5, fill = "Orange")

if __name__ == '__main__':
    root = Tk()
    root.geometry("600x600+300+300")
    app = DistanceFinderFrame(root)
root.mainloop() #Start the GUI
