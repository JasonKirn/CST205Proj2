from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import os
import os.path
import FocalMath
import math

from PIL import Image,ImageTk

"""
Course: CST205-Multimedia Design and Programming
Authors: Mathew Tomberlin (Combining team member components)
         Jason Kirn (GUI Design)
         Phuc Pham (FocalMath class design)
Date: 10/12/2016
Abstract: This application allows the user to select either an image or a text file in order to determine camera
          focal length. The user can enter the estimated object size and distance to camera in order to determine
          the focal length. Once the focal length is determined, it is saved out to a text file so that it may be
          reused later. With the focal length, the user can select an image and find the distance to a subject by
          entering the apparent image size in pixels.
"""

#These fonts are used for the application's labels and buttons
TITLE_FONT = ("Helvetica", 18, "bold", "underline")
LABEL_FONT = ("Helvetica", 12, "bold")
BODY_FONT = ("Helvetica", 11)

#A utility method that tries to parse a string as a float and returns None if it fails
def try_parse(string, fail=None):
    try:
        return float(string)
    except:
        return fail;

"""
Abstract: This class represents the view controller for the entire application. Because this is a simple application,
          we use only one view controller. The view controller has a stack of pages of the application (the top-most
          of which is visible). It holds the references to the estimated size, estimated distance and calculated distance
          text variables.
"""

class AppController(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        #The container holds the stack of pages (frames), with the topmost frame being currently visible

        #Configure the container
        container = Frame(self)
        container.pack(side="top",fill="both",expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        #This is the stack of pages (frames)
        self.frames = {}

        #These are String variables that are used by the text entries and labels of various screens
        self.estimated_size_text = StringVar()
        self.estimated_distance_text = StringVar()
        self.calculated_distance_text = StringVar()

        #Add and configure each page on the stack
        for F in (SelectCalibration, SelectImage, FindFocalLength, FindDistance):
            page_name = F.__name__
            frame = F(container,self)
            self.frames[page_name] = frame
            frame.grid(row=0,column=0, sticky="nsew")

        #Raise SelectCalibration to the top of the page stack
        self.show_frame("SelectCalibration")

    #Raises the frame to the top of the stack
    def show_frame(self, page_name):
        global click_points
        global click_count

        #If the frame is the SelectImage pages...
        if(page_name is "SelectImage"):
            #Set the estimated distance, estimated size and calculated distance to their defaults for this screen
            self.estimated_distance_text.set(0)
            self.estimated_size_text.set(0)
            self.calculated_distance_text.set("Not Yet Calculated!")
            #Reset the click points
            click_points = {}
            click_count = 0
            canvas.delete("all")
        elif(page_name is "SelectCalibration"):
            # Set the estimated distance, estimated size and calculated distance to their defaults for this screen
            self.estimated_distance_text.set(1)
            self.estimated_size_text.set(11)
            self.calculated_distance_text.set(0)
            # Reset the click points
            click_points = {}
            click_count = 0
            calibration_canvas.delete("all")
        frame=self.frames[page_name]
        frame.tkraise()

    def select_image(self,calibration=TRUE):
        global filename
        #Open a file selection dialog.
        filename = askopenfilename()

        #Try to load the image to image
        self.try_load_selected_image(calibration)

        #If the image is loaded properly...
        #(If not, nothing else happens and the user can select another image)
        if(filename is not None):
            #If the user is selecting an image for calibration, go to the FindFocalLength page
            if calibration is TRUE:
                self.show_frame("FindFocalLength")
            #Otherwise, go to the FindDistance page
            else:
                self.show_frame("FindDistance")

    def select_calibration_file(self):
        global filename
        # Open a file selection dialog.
        filename = askopenfilename()

        #Try to load the text file in to the focal_length and estimated_size variables
        self.try_load_selected_file()

        #If the text file is loaded properly...
        #(If not, nothing happens and the user can select another file)
        if(filename is not None):
            #Go to the SelectImage page
            self.show_frame("SelectImage")

    #Try to open filename and assign the image to image
    #If that fails, show an error message and set filename to None
    def try_load_selected_image(self,calibration):
        global image
        global filename
        global processed_image
        global canvas
        global calibration_canvas

        try:
            image = Image.open(filename)

            # Load selected image to canvas
            image.thumbnail((512, 512), Image.ANTIALIAS)
            processed_image = ImageTk.PhotoImage(image)

            if(calibration is TRUE):
                calibration_canvas.create_image(0, 0, anchor=NW, image=processed_image)
            else:
                canvas.create_image(0,0, anchor=NW, image=processed_image)
        except:
            showerror("Error", "Invalid file or directory!")
            filename = None


    #Try to open filename and assign the lines in the text file to the 'content' list
    #If that succeeds, read the first two lines and get the focal_length and estimated_size

    #If either of the above fails (For invalid file type, casting, insufficient number of lines, etc), show an
    #error and set filename to None
    def try_load_selected_file(self):
        global focal_length
        global estimated_size
        global filename

        try:
            with open(filename) as f:
                content = f.readlines()

            for line in content:
                i = 0
                if try_parse(line) is not None:
                    i+=1
                    if i is 1:
                        focal_length = float(line)
        except:
            showerror("Error", "Invalid file or directory!")
            filename = None

    #Select a point and draw the line when the user clicks the calibration canvas
    def calibration_mouse_click(self,event):
        global click_count

        self.select_point(event, TRUE)

        if(click_count==1):
            self.draw_line(TRUE)
        else:
            click_count+=1

    # Select a point and draw the line when the user clicks the calibration canvas
    def mouse_click(self,event):
        global click_count

        self.select_point(event, FALSE)

        if (click_count == 1):
            self.draw_line(FALSE)
        else:
            click_count += 1

    #Assign point to dictionary and draw rect
    def select_point(self, event, calibration):
        global canvas
        global calibration_canvas
        global click_points
        global click_count

        if(calibration is TRUE):
            calibration_canvas.create_rectangle(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="blue")
        else:
            canvas.create_rectangle(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="blue")

        click_points[click_count] = (event.x, event.y)

    #Draw a line between points
    def draw_line(self, calibration):
        global canvas
        global calibration_canvas
        global click_points
        global click_count

        global pixelWidth

        x1 = click_points[click_count - 1][0]
        y1 = click_points[click_count - 1][1]
        x2 = click_points[click_count][0]
        y2 = click_points[click_count][1]
        if(calibration is TRUE):
            calibration_canvas.create_line(x1, y1, x2, y2)
        else:
            canvas.create_line(x1, y1, x2, y2)

        pixelWidth = FocalMath.distance(click_points[click_count - 1], click_points[click_count])
        print(pixelWidth)

    def find_focal_length(self):
        global focal_length

        if(self.estimated_distance_text.get() != "") and (float(self.estimated_distance_text.get()) > 0) and (self.estimated_distance_text.get() != "") and (float(self.estimated_size_text.get()) > 0) and (self.estimated_size_text.get() != "") and pixelWidth > 0:
            print("Estimated Distance: " + self.estimated_distance_text.get() + ", Estimated Size: " + self.estimated_size_text.get() + ",Pixel Width: " + str(pixelWidth))
            focal_length = FocalMath.calculatefocal(float(self.estimated_distance_text.get()), float(pixelWidth), float(self.estimated_size_text.get()))
            print("Calculated FOV: " + str(focal_length))

            self.show_frame("SelectImage")

    def find_distance(self):

        if (self.estimated_size_text.get() != "") and (float(self.estimated_size_text.get()) > 0) and focal_length > 0 and pixelWidth > 0:
            print("Focal Length: " + str(focal_length) + ", Estimated Width in Real Life: " + self.estimated_size_text.get() + ",Pixel Width: " + str(pixelWidth))
            distance = FocalMath.calculatedistance(float(focal_length), float(self.estimated_size_text.get()), float(pixelWidth))
            print("Distance: "+str(distance))
            return distance

"""
The layout of the Calibration File/Image selection screen
"""
class SelectCalibration(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        #Set this page's controller to the main AppController
        self.controller = controller

        #Declare a label on this page using the title font and pack it at the top of the frame
        title = Label(self, text="Select a Calibration File or Image", font = TITLE_FONT)
        title.pack(side = TOP, anchor = N)

        #Two buttons for selecting either and image or a text file. The button command is a function in the controller that
        #allows the selection of files from a dialog window.
        select_image_bttn = Button(self, text="Select Calibration Image", command=controller.select_image)
        select_file_bttn = Button(self, text="Select Calibration File", command=controller.select_calibration_file)

        #Pack both buttons in a stack on the window
        select_image_bttn.pack(side = TOP, anchor = N)
        select_file_bttn.pack(side = TOP, anchor = N)

"""
The layout of the Image selection screen
"""
class SelectImage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #Set this page's controller to the main AppController
        self.controller = controller

        #Declare a label on this page using the title font and pack it at the top of the frame
        title = Label(self, text="Select Image", font=TITLE_FONT)
        title.pack(side="top", fill="x", pady=10)

        #Declare a button for selecting an image. This is not a configuration image (configuration=FALSE). Pack it on the
        #frame stack
        button = Button(self, text="Select Image", command=lambda: controller.select_image(FALSE), font=LABEL_FONT)
        button.pack()

"""
The layout of the Find Focal Length screen and methods for saving the calibration file
"""
class FindFocalLength(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        global calibration_canvas

        # Set this page's controller to the main AppController
        self.controller = controller

        # Declare a label on this page using the title font and pack it at the top of the frame
        title = Label(self, text="Find Focal Length", font=TITLE_FONT)
        title.grid(row=0,column=1)

        est_size_label = Label(self, text="Estimated Width in Real Life", font=LABEL_FONT)
        est_size_label.grid(row=1,column=0, sticky = "e")

        estimated_size_entry = Entry(self, textvariable=self.controller.estimated_size_text)
        estimated_size_entry.grid(row=1,column=1)

        est_distance_label = Label(self, text="Estimated Distance to Object", font=LABEL_FONT)
        est_distance_label.grid(row=2,column=0, sticky = "e")

        estimated_distance_entry = Entry(self, textvariable=self.controller.estimated_distance_text)
        estimated_distance_entry.grid(row=2,column=1)

        # Declare a button for calculating the focal length, given the pixel width of the object,
        # estimated distance and estimated width. Pack it on the frame stack
        button = Button(self, text="Find Focal Length", command=self.find_focal_length_click, font=LABEL_FONT)
        button.grid(row=3,column=1)

        #The image is packed in to the canvas when the image is selected instead of when the frame is created
        calibration_canvas = Canvas(self, width=800, height=500)
        calibration_canvas.grid(row=4,column=0,rowspan=4)
        calibration_canvas.bind("<Button-1>", self.controller.calibration_mouse_click)

    def find_focal_length_click(self):
        self.controller.find_focal_length()
        self.save_calibration()

    def save_calibration(self):
        global focal_length
        i = 0
        while os.path.exists("CalibrationFile" + str(i) + ".txt") is True:
            i += 1

        print("New Calibration File Saved as CalibrationFile" + str(i) + ".txt")

        with open("CalibrationFile" + str(i) + ".txt", 'a') as file:
            file.write(str(focal_length) + "\n")
"""
The layout of the Find Distance screen
"""
class FindDistance(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        global canvas

        # Set this page's controller to the main AppController
        self.controller = controller

        # Declare a label on this page using the title font and pack it at the top of the frame
        title = Label(self, text="Find Distance To Object", font=TITLE_FONT)
        title.pack(side="top", fill="x", pady=10)

        distance_display_label = Label(self, text="Calculated Distance to Object", font=LABEL_FONT)
        distance_display_label.pack()

        distance_label = Label(self, textvariable=self.controller.calculated_distance_text)
        distance_label.pack()

        est_size_label = Label(self, text="Estimated Width in Real Life", font=LABEL_FONT)
        est_size_label.pack()

        estimated_size_entry = Entry(self, textvariable=self.controller.estimated_size_text)
        estimated_size_entry.pack()

        # Declare a button for calculating the focal length, given the pixel width of the object,
        # estimated distance and estimated width. Pack it on the frame stack
        find_distance_button = Button(self, text="Find Distance to Object", command=self.find_distance_click, font=LABEL_FONT)
        find_distance_button.pack()

        # Declare a button for calculating the focal length, given the pixel width of the object,
        # estimated distance and estimated width. Pack it on the frame stack
        change_calibration_button = Button(self, text="Change Calibration File", command=self.change_calibration_click)
        change_calibration_button.pack()

        # Declare a button for calculating the focal length, given the pixel width of the object,
        # estimated distance and estimated width. Pack it on the frame stack
        select_image_button = Button(self, text="Select New Image", command=self.select_image_click)
        select_image_button.pack()

        #The image is packed in to the canvas when the image is selected instead of when the frame is created
        canvas = Canvas(self, width=800, height=500)
        canvas.pack()
        canvas.bind("<Button-1>", controller.mouse_click)

    def find_distance_click(self):

        self.controller.calculated_distance_text.set(self.controller.find_distance())

    def change_calibration_click(self):

        self.controller.show_frame("SelectCalibration")

    def select_image_click(self):

        self.controller.show_frame("SelectImage")

"""
Global fields and references as well as the entry point of the application
"""
if __name__ == "__main__":
    #Global fields
    focal_length = 0.0
    estimated_size = 0.0
    estimated_distance = 0.0
    pixelWidth = 0.0
    calculated_distance = 0.0
    click_points = {}
    click_count = 0

    #Global element references
    filename = None
    image = None
    calibration_canvas = None
    canvas = None
    processed_image = None

    app = AppController()
    app.overrideredirect(True)
    app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight()))
    app.focus_set()  # <-- move focus to this widget
    app.bind("<Escape>", lambda e: app.quit())
app.mainloop()
