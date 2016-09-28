import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from PIL import Image,ImageTk


def try_parse(string, fail=None):
    try:
        return float(string)
    except Exception:
        return fail;
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
class MenuFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="grey")
        """
        Declaring instance variables:
        Some of these lines are technically redundant
        But its good to have a list of your class's instance variables
        in one easy-to-locate place as opposed to simply
        declaring and assigning them when you use them.
        """
        self.parent = parent

        self.calibration_filename = ""
        self.image_filename = ""
        self.image = None
        self.processed_image = None

        # GUI references
        self.estimated_size_entry = 0
        self.estimatedsize_label = None
        self.estimated_distance_entry = 0
        self.estimateddistance_label = None
        self.menu_label = None
        self.finddistance_button = None
        self.calibrationfile_button = None
        self.calibrationimage_button = None

        # Create calibration file selection menu
        self.show_calibration_view()

    #Create the two buttons that make up the calibration selection menu
    def show_calibration_view(self):

        self.calibrationfile_button = Button(self, text='Select Calibration File', command=self.select_calibration_file_dialog)
        self.calibrationfile_button.grid(row=1, column=0)
        self.calibrationimage_button = Button(self, text='Select Calibration Image', command=self.select_calibration_image_dialog)
        self.calibrationimage_button.grid(row=2, column=0)

    # First ask the user for a file, then load the values from that file and then show the menu items for finding the distance
    def select_calibration_file_dialog(self):
        self.calibration_filename = askopenfilename()

        self.load_calibration_file()
        self.show_finddistance_view()

    #First ask the user for a file, then load the image from that file and then show the menu items for finding the distance
    def select_calibration_image_dialog(self):
        self.image_filename = askopenfilename()

        self.load_selected_image()
        self.show_finddistance_view()

    # Display the view in which the user can select a pixel width and actual width
    def show_finddistance_view(self):
        if (self.image_filename is not None) or (menu.calibration_filename is not None):
            # Clear Calibration Selection buttons
            self.calibrationfile_button.grid_forget()
            self.calibrationimage_button.grid_forget()
            self.grid_forget()

            #Createa a label and a text entry for the estimated size
            #Because this image is recommended to be an 8.5" x 11" piece of paper we default this value to 11"
            menu.estimated_size = 11
            self.estimatedsize_label = Label(self,text="Estimated Size: ")
            self.estimatedsize_label.grid(row=0, column=0)

            self.estimated_size_content = StringVar()
            self.estimated_size_entry = Entry(self,text=str(menu.estimated_size),textvariable=self.estimated_size_content)
            self.estimated_size_content.set(menu.estimated_size)
            self.estimated_size_entry.delete(0, END)
            self.estimated_size_entry.insert(0, menu.estimated_size)
            self.estimated_size_entry.grid(row=0, column=1)

            # Createa a label and a text entry for the estimated distance
            # Because this image is recommended to be an 1 foot away, we default this value to 1
            menu.estimated_distance = 1.0
            self.estimatedsize_label = Label(self, text="Estimated Distance: ")
            self.estimatedsize_label.grid(row=1, column=0)

            self.estimated_distance_content = StringVar()
            self.estimated_distance_entry = Entry(self, text=str(menu.estimated_size), textvariable=self.estimated_distance_content)
            self.estimated_distance_content.set(menu.estimated_distance)
            self.estimated_distance_entry.delete(0, END)
            self.estimated_distance_entry.insert(0, menu.estimated_distance)
            self.estimated_distance_entry.grid(row=1, column=1)

            self.grid(row=1, column=0, sticky=NW)#updated here: Jason

    #When the user has clicked twice on the canvas, display the 'Find Distance' button in the menu
    def show_finddistance_button(self):
        self.finddistance_button = Button(self, text='Find Distance', command=canvasframe.find_distance)
        self.finddistance_button.grid(row=2, column=0, columnspan=2)
        self.grid(row=1, column=0, sticky=NW)#updated here: Jason

    #If the file can be loaded as an image, load it as an image and create it on the canvas
    def load_selected_image(self):
        if (self.image_filename is not ""):
            try:
                self.image = Image.open(self.image_filename)
            except:
                showerror("Error", "Invalid file or directory!")
                self.image_filename = None

            if (self.image_filename is not None):
                # Load selected image to canvas
                self.image.thumbnail((512, 512), Image.ANTIALIAS)
                self.processed_image = ImageTk.PhotoImage(self.image)
                canvasframe.canvas.create_image(0, 0, anchor=NW, image=self.processed_image)

    #If the file can be loaded as a text file, load it and read the values in
    def load_calibration_file(self):
        if (self.calibration_filename is not None):
            try:
                self.calibration_file = open(self.calibration_filename, "r")
            except:
                showerror("Error", "Invalid file or directory!")
                self.calibration_file = None

            if (self.calibration_file is not None):
                i = 0
                for line in self.calibration_file:
                    if try_parse(line) is not None:
                        i += 1
                        if(i is 1):
                            # Get the FOV from the first line of the file
                            canvasframe.FOV = float(line)
                        elif(i is 2):
                            #Get the estimated size of the object (11")
                            canvasframe.estimated_size = float(line)

class DistanceFinderFrame(Frame):


    """
    Event: Mouse Click
    Bound To: Canvas
    Abstract: Given the mouse_click event coordinates (event.x and event.y), if we haven't described an apparent pixel
              width yet (self.pixelWidth), assign the mouse_click event coordinates to an integer index
              (self.click_count) in the self.click_points array.
    """
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
        self.canvas.grid()

        #Input
        self.click_points = {}
        self.click_count = 0

        #Per image pixel width
        self.pixelWidth = None
        #Per camera settings
        self.FOV = 0.0

        #Create initial GUI
        self.init_ui()

    def init_ui(self):
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

    def mouse_click(self,event):
        if(self.pixelWidth is None and menu.image_filename is not ""):
            self.select_point(event)

            if(self.click_count%2==1):
                menu.show_finddistance_button()
                self.draw_line()
                self.click_count = 0
                return
            self.click_count = self.click_count + 1

    def select_point(self, event):
        canvasframe.canvas.create_rectangle(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="blue")
        self.click_points[self.click_count] = (event.x, event.y)

    def draw_line(self):
        x1 = self.click_points[self.click_count - 1][0]
        y1 = self.click_points[self.click_count - 1][1]
        x2 = self.click_points[self.click_count][0]
        y2 = self.click_points[self.click_count][1]
        canvasframe.canvas.create_line(x1, y1, x2, y2)

    def find_distance(self):
        self.estimated_size = menu.estimated_size_content.get()
        self.estimated_distance = menu.estimated_distance_content.get()

        self.distance = self.estimated_size
        self.distance_text = "Distance: " + str(self.distance);

        self.text = self.canvas.create_text(0, 0, anchor="nw")
        self.canvas.itemconfig(self.text, text=self.distance_text)
        self.canvas.insert(self.text, 0, "")

"""
Global Variables:
The variables declared and assigned to in this scope (root and app in this case)
are usable anywhere on this script (and should be usable by scripts that import
this script)
"""
if __name__ == '__main__':
    root = Tk()
    root.geometry("800x500+300+300")

    #Create a frame for the canvas
    canvasframe = DistanceFinderFrame(root)
    canvasframe.grid(row=2)

    #Create a frame for the menu items
    menu = MenuFrame(root)
    Label(root, text = 'Menu:').grid(row=0,column=0,sticky=NW)#updated here:Jason
    menu.grid(row=1, column=0,sticky=NW)#updated here:Jason

    root.mainloop()
