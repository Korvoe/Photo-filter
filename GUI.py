import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Filter(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.path_to_image_1 = ''

    def browse_button(self):
        self.path_to_image_1 = str(tk.filedialog.askopenfile(initialdir = "/home", title = "Select image",
                                                         filetypes = (("jpeg files","*.jpg"),
                                                                      ("all files","*.*"))).name)

    def show_image_to_process(self):
        self.image_1 = Image.open(self.path_to_image_1)

        ##Saving the width to height proportion and resizing.
        self.width, self.height = self.image_1.size
        self.width_to_height = self.width / self.height

        if self.width > 600:
            self.width = 600
            self.height = int(self.width * self.width_to_height)
        if self.height > 400:
            self.height = 400
            self.width = int(self.height * self.width_to_height)
        self.size_image_1 = (self.width, self.height)

        ##Creating a label to show the image, we are going to process
        self.image_1 = ImageTk.PhotoImage(self.image_1.resize(self.size_image_1), Image.ANTIALIAS)
        self.image_to_process = tk.Label(self.master, image=self.image_1)
        self.image_to_process.place(x = (1000 - self.width) / 2)##Placing the image in the center-top part of a Frame



root = tk.Tk()
root.title("Filter for images")
root.geometry("1000x1000")
root.resizable(0, 0)

Filter_program = Filter(master=root)
Filter_program.browse_button()
Filter_program.show_image_to_process()

Filter_program.mainloop()