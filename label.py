import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
from PIL import ImageTk, Image 
import numpy as np


#GLOBAL VAR
IMAGE_LIST = []
index = 0
CLICK_MAX = 0

LABEL = np.zeros(8)
PATH = 'path_to_save_text_file'


class Application(Frame):
    
    
    def window(self):
        self.geometry('1000x1000')
        self.num_box = 0
        self.box = 0
        
    
    def opendir_button(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        global IMAGE_LIST
        folder_selected = filedialog.askdirectory()
        print("Selected folder: ", folder_selected)

        os.chdir(folder_selected)
        
        IMAGE_LIST = os.listdir(folder_selected)
        assert len(IMAGE_LIST) != 0, "Empty folder!"

    def callback(self, event, size):
        global CLICK_MAX, LABEL          
        self.IMG_BORDER.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3,
                                    fill = 'red', 
                                    tag = 'points' + str(self.num_box))
        
        LABEL[(CLICK_MAX)*2] = event.x
        LABEL[(CLICK_MAX)*2 + 1] = event.y
        
        if CLICK_MAX > 0:
            self.IMG_BORDER.create_line(LABEL[(CLICK_MAX-1)*2], LABEL[(CLICK_MAX-1)*2 + 1], event.x, event.y,
                                        fill = 'green',
                                        dash = (100,100),
                                        tag = 'line'+ str(self.num_box))

        print("clicked at ", event.x," ", event.y)
        CLICK_MAX += 1
        if CLICK_MAX == 4:
            scale_x = size[0]/800
            scale_y = size[1]/500
            self.IMG_BORDER.create_line(LABEL[0], LABEL[1], LABEL[6], LABEL[7],
                                        fill = 'green',
                                        tag = 'line' + str(self.num_box),
                                        dash = (100,100))
            self.IMG_BORDER.unbind("<Button-1>")
            LABEL[::2] *= scale_x
            LABEL[1::2] *= scale_y
        
    def open_image(self, index):
        self.image = Image.open(IMAGE_LIST[index])
        size = self.image.size
        self.image = (self.image).resize((800,500))
        self.image = ImageTk.PhotoImage(self.image)
        return self.image, size

    def next_button(self):
        
        self.num_box = 0
        self.box = 0
        global index
        index += 1
        self.IMG_BORDER = Canvas(self, width = 800, height = 500)
        image, self.size = self.open_image(index)

        self.IMG_BORDER.create_image(400, 250, image = self.image)
        self.IMG_BORDER.grid(column = 2, row = 2)
        
        self.IMG_BORDER.bind("<Button-1>", lambda event, size = self.size: self.callback(event,size = self.size))
        
    def prev_button(self):
        
        global index
        self.num_box = 0
        self.box = 0
        index -= 1
        self.IMG_BORDER = Canvas(self, width = 800, height = 500)
        image, size = self.open_image(index)

        self.IMG_BORDER.create_image(400, 250, image = self.image)
        self.IMG_BORDER.grid(column = 2, row = 2)
        
        self.IMG_BORDER.bind("<Button-1>", lambda event, size = self.size: self.callback(event,size = self.size))


    def reset_button(self):
        global CLICK_MAX, LABEL
        CLICK_MAX = 0
        LABEL = np.zeros(8)
        self.IMG_BORDER.delete('points' + str(self.num_box), 'line' + str(self.num_box))
        self.IMG_BORDER.bind("<Button-1>", lambda event, size = self.size: self.callback(event,size = self.size))

        if (self.num_box > self.box) :
            self.num_box -= 1
        
        print("Reset!")

    def save_button(self):
        
        global CLICK_MAX, LABEL
        
        assert CLICK_MAX == 4, print("You must draw 4 points!")
        
        CLICK_MAX = 0
        self.num_box += 1
        self.box += 1
        self.IMG_BORDER.bind("<Button-1>", lambda event, size = self.size: self.callback(event,size = self.size))

        path = PATH
        self.box = self.num_box #saved box

        with open(path + IMAGE_LIST[index][0:-4] + '.txt', "a") as text_file:
            for i, coordinate in enumerate(LABEL):
                text_file.write(str(int(coordinate))) # 8 elements
                if i != 7 :
                    text_file.write(',')     
            text_file.write("\n")
        
        print("Saved!")
        LABEL = np.zeros(8)
    
 
    def createWidgets(self):          
        
        self.SAVE = Button(self, text = "Save", command = self.save_button)
        self.SAVE.grid(column=1, row = 0)

        self.RESET = Button(self, text = "Reset", command = self.reset_button)
        self.RESET.grid(column = 1, row = 2)

        self.OPEN_DIR = Button(self, text = "Open Direction", command = self.opendir_button)
        self.OPEN_DIR.grid(column = 1, row = 3)

        self.PREV = Button(self, text = "Previous", command = self.prev_button)
        self.PREV.grid(column = 4, row = 3)
        self.NEXT = Button(self, text = "Next", command = self.next_button)
        self.NEXT.grid(column = 5, row = 3)           

        self.QUIT = Button(self, text = "QUIT", fg = "red", command = self.quit )
        self.QUIT.grid(column = 1, row = 4)


    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


root = Tk()
root.title('Text Labeling')
app = Application(master = root)

app.mainloop()
root.destroy()
