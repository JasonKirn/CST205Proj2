
from tkinter import *
from PIL import Image,ImageTk
#import test.py

"""
Authors: Mathew Tomberlin
Abstract: This project takes an image of an 8.5" x 11" piece of paper 1 foot from the camera in order to
          calibrate the camera's Focal Length. Then, given the user's estimate of the object's actual
          width and the user's input of the pixel width, calculate the distance from the object to the camera.
"""


class DistanceFinderFrame(Frame):



    def mouse_click(self,event):
        app.canvas.create_rectangle(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="blue")
        self.click_points[self.click_count] = (event.x, event.y)
        if(self.click_count%2==1):
            x1 = self.click_points[self.click_count-1][0]
            y1 = self.click_points[self.click_count-1][1]
            x2 = self.click_points[self.click_count][0]
            y2 = self.click_points[self.click_count][1]
            app.canvas.create_line(x1,y1,x2,y2)
            self.click_count = 0
            return
        self.click_count = self.click_count + 1

    def find_distance(self):
        text = self.canvas.create_text(256, 30, anchor="nw")
        self.canvas.itemconfig(text, text="Distance: ")
        self.canvas.insert(text, 0, "")

    def __init__(self,parent):
        Frame.__init__(self,parent,background="white")
        self.parent = parent
        self.canvas = Canvas(self, width=800, height=500)
        self.click_points = {}
        self.click_count = 0
        self.init_ui()

    def init_ui(self):
        self.parent.title("Distance Finder")
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.button = Button(self, text='Press Me', command=self.find_distance()).pack()
        self.image = Image.open("Jojo_wolves.jpg")
        self.canvas.create_image(50, 50, anchor=NW, image=self.file_image)
        self.canvas.pack()
        self.pack(fill=BOTH, expand=1)

if __name__ == '__main__':
    root = Tk()
    root.geometry("800x500+300+300")
    app = DistanceFinderFrame(root)
root.mainloop()
