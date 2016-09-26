import tkinter
from PIL import Image, ImageTk
#open a SPIDER image and convert to byte format
im = Image.open(r'tracerSmall.jpg')



root = tkinter.Tk() # A root window for displaying objects
root.title("Korean hack module")
#Convert the Image object into a TkPhoto object
tkimage = ImageTk.PhotoImage(im)



#Put it in a display window
def show_entry_fields():
    print("GG EZ: ")


tkinter.Label(root, image=tkimage, text = "Hackerman was here", fg = "orange", font = ("Helvetica", 20), compound = tkinter.CENTER).pack(side = tkinter.BOTTOM, anchor = tkinter.S)

tkinter.Button(text = "Set Ult to 100%").pack(side= tkinter.TOP, anchor= tkinter.N, expand= tkinter.YES)

tkinter.Label(text="Some info: Don't report pls").pack(side = tkinter.LEFT, anchor = tkinter.N)

tkinter.Label(text="Enter account info for free hacks:").pack(side = tkinter.TOP, anchor = tkinter.N)

tkinter.Button(text = "Quit", command = root.quit).pack(side = tkinter.BOTTOM, anchor = tkinter.W)

tkinter.Button(text = "Enter", command = show_entry_fields).pack(side = tkinter.BOTTOM, anchor = tkinter.S)

E1 = tkinter.Entry(root)

E1.pack(side = tkinter.TOP, anchor = tkinter.N)

root.mainloop() #Start the GUI
