import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk

class Filter(tkinter.Frame):
    def __init__(self, master=None):
        # master is a Root frame.
        super().__init__(master)
        self.master = master
        self.pack()

        #Menu at the top-left part of a screen
        self.show_menu()
        self.master.config(menu=self.menubar)

        ##Frame for filters, as you may notice from the variable`s name
        self.frame_for_filters = tkinter.Frame(self.master, relief=tkinter.SUNKEN,
                                     width = 350, height = 1000, bd = 5)
        self.frame_for_filters.pack(side=tkinter.RIGHT)

        ## Setting a frame and canvas inside of a main frame(master), at which the image will be shown.#####################
        self.image_frame_width = 1200
        self.image_frame_height = 900

        #Frame
        self.image_frame = tkinter.Frame(self.master, relief=tkinter.SUNKEN,
                    width=self.image_frame_width, height=self.image_frame_height, bd=5)
        self.image_frame.pack(side=tkinter.RIGHT)

        #Canvas
        self.image_canvas = tkinter.Canvas(self.image_frame,
                    width=self.image_frame_width, height=self.image_frame_height, bg='black')
        self.image_canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        #######################################################################################################

        ##Frame for something else(No idea for what, but may be useful)
        self.framew_for_filters = tkinter.Frame(self.master, relief=tkinter.SUNKEN,
                                               width=350, height=1000, bd=5)
        self.framew_for_filters.pack(side=tkinter.RIGHT)

    def show_menu(self):
        self.menubar = tkinter.Menu(self.master)
        filemenu = tkinter.Menu(self.menubar)
        ##Creating the File cascade of the menu, with commands "Open", "Save as" and "Quit!"
        self.menubar.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "Open", command = self.open_image)
        filemenu.add_command(label = "Save as", command = self.save_image)
        filemenu.add_separator()
        filemenu.add_command(label = "Quit!", command = root.quit)

    def open_image(self):
        self.path_to_image = str(tkinter.filedialog.askopenfile(title = "Select image",
                                        filetypes = (("jpeg files","*.jpg"), ("all files","*.*"))).name)
        self.show_image()

    def save_image(self):
        path_and_name_to_save = tkinter.filedialog.asksaveasfilename(title = "Save as",
                                        filetypes = (("jpeg files","*.jpg"), ("all files","*.*")))
        self.img.save(path_and_name_to_save)

    def show_image(self):
        self.img = Image.open(self.path_to_image)

        ##Resizing the image to fit in the frame.
        width, height = self.img.size
        if width > self.image_frame_width:
            ratio = height / width
            width = self.image_frame_width
            height = width * ratio
        elif height > self.image_frame_height:
            ratio = width / height
            height = self.image_frame_height
            width = height * ratio
        self.img = self.img.resize((int(width), int(height)), Image.ANTIALIAS)
        ##Placing the image in the center of a Frame, using canvas widget.
        self.image = ImageTk.PhotoImage(self.img)
        self.image_canvas.create_image((self.image_frame_width - width)/2,
                                 (self.image_frame_height - height)/2,
                                         image=self.image, anchor=tkinter.NW)

######################FILTERS##################################################
    def black_and_white(self):
        R, G, B = 0, 1, 2
        source = self.img.split()
        source[B].paste(source[R], None, None)
        source[G].paste(source[R], None, None)
        self.img = Image.merge(self.img.mode, source)

    def high_contrast(self):
        for i in range(0, self.img.size[0]):
            for j in range(0, self.img.size[1]):
                if self.img.getpixel((i, j))[0] + self.img.getpixel((i, j))[1] + self.img.getpixel((i, j))[2] > 366:
                    self.img.putpixel([i, j], (self.img.getpixel((i, j))[0] + 50, self.img.getpixel((i, j))[1] + 50,
                                            self.img.getpixel((i, j))[2] + 50))
                else:
                    self.img.putpixel([i, j], (self.img.getpixel((i, j))[0] - 50, self.img.getpixel((i, j))[1] - 50,
                                            self.img.getpixel((i, j))[2] - 50))

    def negative(self):
        source = self.img.split()

        R, G, B = 0, 1, 2

        red_reverse = source[R].point(lambda i: 255 - i)
        green_reverse = source[G].point(lambda i: 255 - i)
        blue_reverse = source[B].point(lambda i: 255 - i)

        source[R].paste(red_reverse, None, None)
        source[G].paste(green_reverse, None, None)
        source[B].paste(blue_reverse, None, None)

        self.img = Image.merge(self.img.mode, source)
#######################################################################################


##Initialization of the program
root = tkinter.Tk()
root.title("Filter for images")
root.geometry("1800x1000")
Filter_program = Filter(master=root)
Filter_program.mainloop()
