import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from PIL import Image,ImageTk

"""
Authors: Mathew Tomberlin
Abstract: This project takes an image of an 8.5" x 11" piece of paper 1 foot from the camera in order to
          calibrate the camera's Focal Length. Then, given the user's estimate of the object's actual
          width and the user's input of the pixel width, calculate the distance from the object to the camera.

    ================================================Instance Fields (self)==============================================
    Tk parent                               is a reference to the parent window of this frame

    Canvas canvas                           is a reference to the canvas in this frame

    Image image                             is an image loaded by Pillow. After being loaded, we use the thumbnail()
                                            method to scale it down

    ImageTk.PhotoImage processedImage       is the scaled down image in a format tkinter can read

    Button button                           is a tkinter Button widget that, when clicked, calls the find_distance
                                            method via the button command

    Dict click_points                       is a reference to the point structs that represent mouse click positions on
                                            the screen

    int click_count                         is an index which increments when the user clicks. Begins at 0 and counts
                                            to 1, then resets to 0 (Meaning every 3rd and 4th click replaces the 1st and
                                            2nd clicks in the array).

    decimal FOV                             the field of view of the camera used to take the calibration image, or read
                                            from the calibration file
    ================================================/Instance Fields (self)==============================================
"""

"""
    ================================================Python Cliff-Notes==============================================
    The way this class is setup is how basic classes in Python should generally be setup.

    __init__(self,parent):
    in this case is the same as a constructor in other languages, meaning it is the first method called when an instance of
    this class is created.

    In order to create and access instance variables for the class, you must use the self keyword (I.E.
    self.pixelWidth). Instance variables can technically be declared and assigned to at the time of their first use, but
    I like to avoid this where possible for clarity. The instance variable's for the class are declared and assigned their empty
    or default values in the __init__(self,parent) method. Again, not all of these must be declared, this is just to have a
    list all in one place.

    The pack() methods are hard to describe. The pack() method basically just describes how the widget is placed geometrically
    in the gui. In the code below, I used

                    self.button = Button(self, text='Press Me', command=self.find_distance()).pack()

    which just creates a new button on the screen, with the text 'Press Me' and the command pointing to this class's
    find_distance method. But notice that I have to call .pack() when I want to create a new widget. This places the button inside the
     Frame (self in this case). If we'd used

                    self.button = Button(self, text='Press Me', command=self.find_distance()).pack(fill=X)
    then our button would take up the entire width of the Frame (self). You'll also notice that when I use
    canvas.create_rectangle() or canvas.create_image(), I don't need to use pack() because the image/rectange/line
    that is created is not a widget, but instead an effect created on the canvas widget, which is packed already.
"""

class DistanceFinderFrame(Frame):


    """
    Event: Mouse Click
    Bound To: Canvas
    Abstract: Given the mouse_click event coordinates (event.x and event.y), if we haven't described an apparent pixel
              width yet (self.pixelWidth), assign the mouse_click event coordinates to an integer index
              (self.click_count) in the self.click_points array.
    """

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

    def select_calibration_file_dialog(self):
        self.calibration_filename = askopenfilename()

        if (self.calibration_filename is not ""):
            try:
                self.calibration_file = open(self.calibration_filename, "r")
            except:
                showerror("Error", "Invalid file or directory!")
                self.calibration_file = None

            if(self.calibration_file is not None):
                for line in self.calibration_file:
                    if self.try_parse(line) is not None:
                        self.FOV = float(line)
                        self.calibrationfile_button.grid_forget()
                        self.calibrationimage_button.grid_forget()
                        self.grid_forget()
                        self.finddistance_button = Button(self, text='Find Distance', command=self.find_distance)
                        self.finddistance_button.grid(row=0,column=0)
                        self.grid()

    def select_calibration_image_dialog(self):
        self.image_filename = askopenfilename()

        if (self.image_filename is not ""):
            try:
                self.image = Image.open(self.image_filename)
            except:
                showerror("Error","Invalid file or directory!")
                self.image_filename = None

            if(self.image_filename is not None):
                self.image.thumbnail((512, 512), Image.ANTIALIAS)
                self.processed_image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=NW, image=self.processed_image)
                self.calibrationfile_button.grid_forget()
                self.calibrationimage_button.grid_forget()
                self.grid_forget()
                self.finddistance_button = Button(self, text='Find Distance', command=self.find_distance)
                self.finddistance_button.grid(row=0, column=0)
                self.grid()

    def find_distance(self):
        text = self.canvas.create_text(256, 30, anchor="nw")
        self.canvas.itemconfig(text, text="Distance: ")
        self.canvas.insert(text, 0, "")

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
        self.calibration_filename = ""
        self.image_filename = ""
        self.image = None
        self.processed_image = None

        self.pixelWidth = None
        self.FOV = 0.0

        self.init_ui()

    def init_ui(self):
        #I like to pack the widgets early if possible
        #self.sizeinput_label = Label(self, text="Actual Size: ")
        #self.sizeinput_label.grid(row=0, column=0)
        self.sizeinput_box = Text(self,width=5,height=1)
        self.sizeinput_box.grid(row=0, column=0)
        self.calibrationfile_button = Button(self, text='Select Calibration File', command=self.select_calibration_file_dialog)
        self.calibrationfile_button.grid(row=1,column=0)
        self.calibrationimage_button = Button(self, text='Select Calibration Image', command=self.select_calibration_image_dialog)
        self.calibrationimage_button.grid(row=2,column=0)
        self.canvas.grid()
        self.grid(row=2)

        #Set the Root window title and bind the mouse_click callback to the canvas
        self.parent.title("Distance Finder")
        self.canvas.bind("<Button-1>", self.mouse_click)

        #Load the image
        #TODO: Load the calibration file if it exists
        #       The calibration file will hold a reference to the camera FOV
        #TODO: Ask for a calibration picture if calibration file does not exist
        #       The calibration file will be generated from the calibration picture
        #TODO: Ask for the subject images
        #       The subject images will be presented one at a time for the user
        #       to input estimated size and apparent width of subject
        #TODO: Output subject images with distance superimposed on image AND/OR distance in textfile
        #       Before processing subject images, the application will ask if the user would
        #       like the distances super imposed on the image, in a seperate text file or both
    def try_parse(string, fail=None):
        try:
            return float(string)
        except Exception:
            return fail;

"""
Global Variables:
The variables declared and assigned to in this scope (root and app in this case)
are usable anywhere on this script (and should be usable by scripts that import
this script)
"""
if __name__ == '__main__':
    root = Tk()
    root.geometry("800x500+300+300")
    app = DistanceFinderFrame(root)
    app2 = DistanceFinderFrame(root)
    root.mainloop()