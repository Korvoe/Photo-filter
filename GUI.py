import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import ctypes
import math

##Screen resolution
screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

class Filter(tkinter.Frame):
    def __init__(self, master = None):
        
        # master is a Root frame.
        super().__init__(master)
        self.master = master
        self.pack()

        #Menu at the top-left part of a screen
        self.show_menu()
        self.master.config(menu = self.menubar)

        #Initialization of size and self.img
        self.img = 0
        self.image_frame_width = screen_width / 1.5
        self.image_frame_height = screen_height
        self.frame_for_configurations_width = screen_width / 6
        self.frame_for_configurations_height = screen_height
        self.frame_for_filters_width = screen_width / 6
        self.frame_for_filters_height = screen_height
        
        ##Frame for something else(No idea for what, but may be useful)
        self.frame_for_configurations = tkinter.Frame(self.master, bd = 3, relief = tkinter.SUNKEN,
                                               width = self.frame_for_configurations_width, height = self.frame_for_configurations_height)
        self.frame_for_configurations.pack(sid = tkinter.RIGHT)
        self.frame_for_configurations.pack_propagate(0)

        ##Setting a frame and canvas inside of a main frame(master), at which the image will be shown.
        #######################################################################################################
        

        #Frame
        self.image_frame = tkinter.Frame(self.master, relief = tkinter.SUNKEN,
                    width = self.image_frame_width, height = self.image_frame_height, bd = 5)
        self.image_frame.pack(side = tkinter.RIGHT)

        #Canvas
        self.image_canvas = tkinter.Canvas(self.image_frame,
                    width = self.image_frame_width, height = self.image_frame_height)
        self.image_canvas.pack(expand = tkinter.YES, fill = tkinter.BOTH)
        #######################################################################################################

        ##Frame for filters, as you may notice from the variable`s name
        self.frame_for_filters = tkinter.Frame(self.master, bd = 3, relief = tkinter.SUNKEN,
                                     width = self.frame_for_filters_width, height = self.frame_for_filters_height)
        self.frame_for_filters.pack(side = tkinter.RIGHT, expand = 1)
        self.frame_for_filters.pack_propagate(0)
    
    def show_menu(self):
        self.menubar = tkinter.Menu(self.master)
        filemenu = tkinter.Menu(self.menubar)

        ##Creating the File cascade of the menu, with commands "Open", "Save as" and "Quit!"
        self.menubar.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "Open", command = self.open_image)
        filemenu.add_command(label = "Save", command = self.save_image)
        filemenu.add_command(labe = "Save as", command = self.save_image_as)
        filemenu.add_separator()
        filemenu.add_command(label = "Quit", command = self.master.destroy)

    def choose_filter(self):
        self.v = tkinter.IntVar(None, 1)

        ##Creating radiobutton for each filter.
        tkinter.Radiobutton(self.frame_for_filters, text = "Original", variable = self.v, value = 1,
                            command = self.original, pady = 5).pack(anchor = tkinter.N)
        tkinter.Radiobutton(self.frame_for_filters, text = "Black and White", variable = self.v, value = 2,
                            command = self.black_and_white, pady = 5).pack(anchor = tkinter.N)
        tkinter.Radiobutton(self.frame_for_filters, text = "Negative", variable = self.v, value = 3,
                            command = self.negative, pady = 5).pack(anchor = tkinter.N)

    def image_configurations(self):
##################################
        brightness_var = ""
        brightness_frame = tkinter.Frame(self.frame_for_configurations, bd = 3, relief = tkinter.SUNKEN)
        brightness_frame.pack(side = "top")
        brightness_label = tkinter.Label(brightness_frame, text = "Brightness settings")
        brightness_label.pack()
        brightness_scale = tkinter.Scale(brightness_frame, orient = tkinter.HORIZONTAL, command = self.change_brightness,
                                         length = self.frame_for_configurations_width, from_ = -255, to = 255, variable = brightness_var)
        brightness_scale.set(0)
        brightness_scale.pack()

##################################
        second_row_frame = tkinter.Frame(self.frame_for_configurations, bd = 3, relief = tkinter.SUNKEN)
        second_row_frame.pack(side = "top")
        
        contrast_var = ""
        contrast_frame = tkinter.Frame(second_row_frame, bd = 3, relief = tkinter.SUNKEN)
        contrast_frame.pack(side = "left")
        contrast_label = tkinter.Label(contrast_frame, text = "Contrast settings")
        contrast_label.pack()
        contrast_scale = tkinter.Scale(contrast_frame, orient = tkinter.VERTICAL, command = self.change_contrast, length = 100, 
                                        from_ = 0, to = 100, variable = contrast_var)
        contrast_scale.pack()

        saturation_var = ""
        saturation_frame = tkinter.Frame(second_row_frame, bd = 3, relief = tkinter.SUNKEN)
        saturation_frame.pack(side = "left")
        saturation_label = tkinter.Label(saturation_frame, text = "Rotation")
        saturation_label.pack()
        saturation_scale = tkinter.Scale(saturation_frame, orient = tkinter.VERTICAL, length = 100, command = self.saturation,
                                              from_ = -100, to = 100, variable = saturation_var)
        saturation_scale.pack()
##################################

        flip_frame = tkinter.Frame(self.frame_for_configurations, bd = 3, relief = tkinter.SUNKEN)
        flip_frame.pack(side = "top")

        flip_label = tkinter.Label(flip_frame, text = "Image flip")
        horizontal_flip_value = ""
        horizontal_flip_checkbutton = tkinter.Checkbutton(flip_frame, text = "Horizontal flip", variable = horizontal_flip_value,
                                              command = self.horizontal_flip, onvalue = 1, offvalue = 0)
        vertical_flip_value = ""
        vertical_flip_checkbutton = tkinter.Checkbutton(flip_frame, text = "Vertical flip", variable = vertical_flip_value,
                                              command = self.vertical_flip, onvalue = 1, offvalue = 0)
        flip_label.pack()
        horizontal_flip_checkbutton.pack()
        vertical_flip_checkbutton.pack()
##################################
        
    def saturation(self, var):
        converter = ImageEnhance.Color(self.img)
        self.image = converter.enhance((100 - int(var)) / 100)
        self.show_image()

    def horizontal_flip(self):
        rotated_image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.image = rotated_image
        self.show_image()

    def vertical_flip(self):
        rotated_image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.image = rotated_image
        self.show_image()
    
    def change_contrast(self, var):
        R, G, B = 0, 1, 2
        source = self.img.split()
        contrast_factor = (259 * (int(var) + 255)) / (255 * (259 - int(var)))
        
        red = source[R].point(lambda i: 128 + contrast_factor * (i - 128))
        green = source[G].point(lambda i: 128 + contrast_factor * (i - 128))
        blue = source[B].point(lambda i: 128 + contrast_factor * (i - 128))
        
        source[R].paste(red, None, None)
        source[G].paste(green, None, None)
        source[B].paste(blue, None, None)
        self.image = Image.merge(self.img.mode, source)
        self.show_image()
    
    def change_brightness(self, var):
        R, G, B = 0, 1, 2
        source = self.img.split()

        red = source[R].point(lambda i: i + int(var))
        green = source[G].point(lambda i: i + int(var))
        blue = source[B].point(lambda i: i + int(var))
        
        source[R].paste(red, None, None)
        source[G].paste(green, None, None)
        source[B].paste(blue, None, None)
        self.image = Image.merge(self.img.mode, source)
        self.show_image()

    def open_image(self):
        ##Opening the image. "self.img" will be used as an input for filter methods
        ## and "self.image" will be used to keep an output of filter methods.
        self.path_to_image = str(tkinter.filedialog.askopenfile(title = "Select image",
                                        filetypes = (("jpeg files","*.jpg"), ("all files","*.*"))).name)
        if self.img == 0:
            self.choose_filter()
            self.image_configurations()

        self.img = Image.open(self.path_to_image)
        self.image = self.img

        self.show_image()

    def save_image(self):
        self.image.save(self.path_to_image)

    def save_image_as(self):
        ##Saving an image in the chosen destination and with chosen name.
        path_and_name_to_save = tkinter.filedialog.asksaveasfilename(title = "Save as",
                                        filetypes = (("jpeg files","*.jpg"), ("all files","*.*")))
        self.image.save(path_and_name_to_save)

    def show_image(self):
        ##Resizing the image to fit in the frame.
        self.width, self.height = self.image.size
        if self.width > self.image_frame_width:
            ratio = self.height / self.width
            self.width = self.image_frame_width
            self.height = self.width * ratio
        elif self.height > self.image_frame_height:
            ratio = self.width / self.height
            self.height = self.image_frame_height
            self.width = self.height * ratio
        self.image = self.image.resize((int(self.width), int(self.height)), Image.ANTIALIAS)

        ##Placing the image in the center of a Frame, using canvas widget.
        self.image_for_canvas = ImageTk.PhotoImage(self.image)
        self.image_canvas.create_image((self.image_frame_width - self.width)/2,
                                 (self.image_frame_height - self.height)/2,
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
root.geometry(str(screen_width)+"x"+str(screen_height))
Filter_program = Filter(master = root)
Filter_program.mainloop()
