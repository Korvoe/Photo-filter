import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk

class Filter(tkinter.Frame):
    def __init__(self, master = None):

        # master is a Root frame.
        super().__init__(master)
        self.master = master
        self.pack()

        #Menu at the top-left part of a screen
        self.show_menu()
        self.master.config(menu = self.menubar)

        ##Frame for something else(No idea for what, but may be useful)
        self.frame_for_customization = tkinter.LabelFrame(self.master,
                                               width = 350, height = 1000)
        self.frame_for_customization.pack(side = tkinter.RIGHT)

        ##Setting a frame and canvas inside of a main frame(master), at which the image will be shown.
        #######################################################################################################
        self.image_frame_width = 1200
        self.image_frame_height = 900

        #Frame
        self.image_frame = tkinter.LabelFrame(self.master, relief = tkinter.SUNKEN,
                    width = self.image_frame_width, height = self.image_frame_height, bd = 5)
        self.image_frame.pack(side = tkinter.RIGHT)

        #Canvas
        self.image_canvas = tkinter.Canvas(self.image_frame,
                    width = self.image_frame_width, height = self.image_frame_height)
        self.image_canvas.pack(expand = tkinter.YES, fill = tkinter.BOTH)
        #######################################################################################################

        ##Frame for filters, as you may notice from the variable`s name
        self.frame_for_filters = tkinter.LabelFrame(self.master,
                                     width = 350, height = 1000)
        self.frame_for_filters.pack(side = tkinter.RIGHT)


    def show_menu(self):
        self.menubar = tkinter.Menu(self.master)
        filemenu = tkinter.Menu(self.menubar)

        ##Creating the File cascade of the menu, with commands "Open", "Save as" and "Quit!"
        self.menubar.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "Open", command = self.open_image)
        filemenu.add_command(label = "Save as", command = self.save_image)
        filemenu.add_separator()
        filemenu.add_command(label = "Quit!", command = root.quit)

    def choose_filter(self):
        self.v = tkinter.IntVar(None, 0)

        ##Creating radiobutton for each filter.
        tkinter.Radiobutton(self.frame_for_filters, text = "Original", variable = self.v, value = 0,
                            command = self.original, pady = 5).pack(anchor = tkinter.W)
        tkinter.Radiobutton(self.frame_for_filters, text = "Black and White", variable = self.v, value = 1,
                            command = self.black_and_white, pady = 5).pack(anchor = tkinter.W)
        tkinter.Radiobutton(self.frame_for_filters, text = "Negative", variable = self.v, value = 2,
                            command = self.negative, pady = 5).pack(anchor = tkinter.W)

    def open_image(self):
        ##Opening the image. "self.img" will be used as an input for filter methods
        ## and "self.image" will be used to keep an output of filter methods.
        self.path_to_image = str(tkinter.filedialog.askopenfile(title = "Select image",
                                        filetypes = (("jpeg files","*.jpg"), ("all files","*.*"))).name)
        self.img = Image.open(self.path_to_image)
        self.image = self.img

        self.show_image()
        self.choose_filter()

    def save_image(self):
        ##Saving an image in the chosen destination and with chosen name.
        path_and_name_to_save = tkinter.filedialog.asksaveasfilename(title = "Save as",
                                        filetypes = (("jpeg files","*.jpg"), ("all files","*.*")))
        self.image.save(path_and_name_to_save)

    def show_image(self):
        ##Resizing the image to fit in the frame.
        width, height = self.image.size
        if width > self.image_frame_width:
            ratio = height / width
            width = self.image_frame_width
            height = width * ratio
        elif height > self.image_frame_height:
            ratio = width / height
            height = self.image_frame_height
            width = height * ratio
        self.image = self.image.resize((int(width), int(height)), Image.ANTIALIAS)

        ##Placing the image in the center of a Frame, using canvas widget.
        self.image_for_canvas = ImageTk.PhotoImage(self.image)
        self.image_canvas.create_image((self.image_frame_width - width)/2,
                                 (self.image_frame_height - height)/2,
                                         image = self.image_for_canvas, anchor = tkinter.NW)

######################FILTERS##################################################
    def original(self):
        self.image = self.img
        self.show_image()

    def black_and_white(self):
        R, G, B = 0, 1, 2
        source = self.img.split()
        source[B].paste(source[R], None, None)
        source[G].paste(source[R], None, None)
        self.image = Image.merge(self.img.mode, source)
        self.show_image()

    def negative(self):
        source = self.img.split()
        R, G, B = 0, 1, 2

        red_reverse = source[R].point(lambda i: 255 - i)
        green_reverse = source[G].point(lambda i: 255 - i)
        blue_reverse = source[B].point(lambda i: 255 - i)

        source[R].paste(red_reverse, None, None)
        source[G].paste(green_reverse, None, None)
        source[B].paste(blue_reverse, None, None)

        self.image = Image.merge(self.img.mode, source)
        self.show_image()
#######################################################################################


##Initialization of the program
root = tkinter.Tk()
root.title("Filter for images")
root.geometry("1800x1000")
Filter_program = Filter(master = root)
Filter_program.mainloop()
