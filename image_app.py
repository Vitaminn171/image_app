import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image, ImageGrab
from tkinter import CENTER, filedialog  

root = tk.Tk()
#setting title
root.title("AI image conversion application")
#setting window size
width=1100
height=580
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

#global var
file_path_image_on_shirt = "bmo.png"
file_path_image_background = ""
file_path_image_generate = ""
image_resize_by_button_H = 100
image_resize_by_button_W = 100

image_x = 0
image_y = 0

flag = False

canvasHeight = 350
canvasWidth = 350
canvas = tk.Canvas(root, width=canvasHeight, height=canvasWidth)
canvas.place(x=700, y=150) 
var = tk.IntVar()

#global var


def GButton_ChooseImage_command():
    # Choose file by dialog
    file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.png;*.jpg"), ("All files", "*.*")))

    # open an image file 
    image = Image.open(file_path)
        
    # Resize the image using resize() method
    imgH = 350
    imgW = 350
    resize_image = image.resize((imgH, imgW))
        
    img = ImageTk.PhotoImage(resize_image)
        
    # create label and add resize image
    # label1 = self.GLabel(image=img)
    label_image = tk.Label(image=img)
    label_image.image = img
    label_image.place(x=200,y=150,width=imgH,height=imgW)


def GButton_Generate_command():

    global flag 
    flag = False
    # Get the new image set to Image.open()
    # Below just demo
    # Remember to check null of getting api image
    # if null don't run code of generate image

    path = "bmo.png"
    imgH = 350
    imgW = 350
    img1 = Image.open(path)
    img1 = ImageTk.PhotoImage(img1.resize((imgH,imgW)))

    # Create ImageTk.PhotoImage object from resized image
    canvas.create_image(0, 0, anchor='nw', image=img1)

     # don't delete this
    img3 = Image.open("tshirt.pg")
    img3 = ImageTk.PhotoImage(img3)
    canvas.create_image(50, 50, anchor='nw', image=img3)
    # don't delete this

    canvas.pack()

    
           

def GRadio_1_command():
    global flag 
    flag = True
    # delete old image available on canvas 
    canvas.delete("all")

    # open the background image
    path = "T-Shirt_1.png"
    img1 = Image.open(path)
    img1 = ImageTk.PhotoImage(img1.resize((350,350)))

    # add image to canvas
    canvas.create_image(0, 0, anchor='nw', image=img1)

    # use api image to set on image
    global file_path_image_background

    # define global image by path
    # because the func resize by button need to load the background again
    file_path_image_background = path

    # open the api image
    # add image to canvas
    img2 = Image.open(file_path_image_on_shirt)
    imgHeight = 100
    imgWidth = 100 
    img2 = ImageTk.PhotoImage(img2.resize((imgHeight,imgWidth)))

    global image_x, image_y
    # set the position in the center of background image 
    image_x = canvasHeight/2 - imgHeight/2
    image_y = canvasWidth/2 - imgWidth/2 
    canvas.create_image(image_x, image_y, anchor='nw', image=img2)

    # don't delete this
    img3 = Image.open("tshirt.pg")
    img3 = ImageTk.PhotoImage(img3)
    canvas.create_image(50, 50, anchor='nw', image=img3)
    # don't delete this

    canvas.pack()
    

def GRadio_2_command():
    global flag 
    flag = False
    #this func is delete all object in canvas 
    #and then show the api image on canvas again look like the generate func
    canvas.delete("all")
    img1 = Image.open(file_path_image_on_shirt)
    img1 = ImageTk.PhotoImage(img1.resize((350,350)))
    canvas.create_image(0, 0, anchor='nw', image=img1)


    # don't delete this
    img3 = Image.open("bmo.pg")
    img3 = ImageTk.PhotoImage(img3)
    canvas.create_image(50, 50, anchor='nw', image=img3)
    # don't delete this

    canvas.pack()

def GRadio_3_command():
    global flag 
    flag = True
    # this func the same of the GRadio_1_command
    canvas.delete("all")
    path = "hoodie.jpg"
    img1 = Image.open(path)
    img1 = ImageTk.PhotoImage(img1.resize((350,350)))
    canvas.create_image(0, 0, anchor='nw', image=img1)
    global file_path_image_background
    file_path_image_background = path
    img2 = Image.open(file_path_image_on_shirt)
    imgHeight = 100
    imgWidth = 100 
    img2 = ImageTk.PhotoImage(img2.resize((imgHeight,imgWidth)))
    global image_x, image_y
    # set the position in the center of background image 
    image_x = canvasHeight/2 - imgHeight/2
    image_y = canvasWidth/2 - imgWidth/2 

    canvas.create_image(image_x, image_y, anchor='nw', image=img2)

    # don't delete this even though there are show error  below terminal
    img3 = Image.open("tshirt.pg")
    img3 = ImageTk.PhotoImage(img3)
    canvas.create_image(50, 50, anchor='nw', image=img3)
    # don't delete this

    canvas.pack()

def resize_image(scale):
    # check if the canvas exist any object
    items = canvas.find_enclosed(0, 0, canvas.winfo_width(), canvas.winfo_height())
    global flag 
    # if the have any object in canvas
    # this func will run 
    if flag:    
        if items:
            # use the width and height global to save the value
            global image_resize_by_button_H, image_resize_by_button_W, image_x, image_y
            if scale == "plus":
                if image_resize_by_button_H < 170 and image_resize_by_button_W < 170:

                    # plus 5px (width,height) while click on button +
                    image_resize_by_button_H += 5
                    image_resize_by_button_W += 5

            if scale == "minus":
                if image_resize_by_button_H > 25 and image_resize_by_button_W > 25:
                    image_resize_by_button_H -= 5
                    image_resize_by_button_W -= 5

            # and reload all image include background
            global file_path_image_background
            img1 = Image.open(file_path_image_background)
            img1 = ImageTk.PhotoImage(img1.resize((350,350)))
            canvas.create_image(0, 0, anchor='nw', image=img1)
            img2 = Image.open(file_path_image_on_shirt)
                    
            # set new size to inside image
            img2 = ImageTk.PhotoImage(img2.resize((image_resize_by_button_H,image_resize_by_button_W)))
            if scale == "plus":
                if image_x == 0:
                    image_x = canvasHeight/2 - image_resize_by_button_H/2

            if scale == "minus":
                if image_y == 0:
                    image_y = canvasWidth/2 - image_resize_by_button_W/2

            canvas.create_image(image_x, image_y, anchor='nw', image=img2)

            # don't delete this even though there are show error  below terminal
            img3 = Image.open("tshirt.pg")
            img3 = ImageTk.PhotoImage(img3)
            canvas.create_image(50, 50, anchor='nw', image=img3)
            # don't delete this
            canvas.pack()


def GButton_plus_command():
    resize_image("plus")

def GButton_minus_command():
    resize_image("minus")

def GButton_SaveImage_command():
    # Convert canvas to image
    global flag 
    items = canvas.find_enclosed(0, 0, canvas.winfo_width(), canvas.winfo_height())
    if items:
        x = root.winfo_rootx() + canvas.winfo_x()
        y = root.winfo_rooty() + canvas.winfo_y()
        x1 = x + canvas.winfo_width()
        y1 = y + canvas.winfo_height()
        img = ImageGrab.grab((x,y,x1,y1))
        
        # Show dialog to choose filename
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        
        # Save image
        if file_path:
            img.save(file_path)

def move(direction):
    items = canvas.find_enclosed(0, 0, canvas.winfo_width(), canvas.winfo_height())
    if flag == True:
        if items:
            global image_y,image_x , image_resize_by_button_H, image_resize_by_button_W
            if direction == "up":
                if image_y > 20:
                    image_y -= 5
            if direction == "down":
                if image_y < (350 - image_resize_by_button_H - 20):
                    image_y += 5
            if direction == "left":
                if image_x > 50:
                    image_x -= 5
            if direction == "right":
                if image_x < (350 - image_resize_by_button_W - 65):
                    image_x += 5
            global file_path_image_background
            img1 = Image.open(file_path_image_background)
            img1 = ImageTk.PhotoImage(img1.resize((350,350)))
            canvas.create_image(0, 0, anchor='nw', image=img1)
            img2 = Image.open(file_path_image_on_shirt)
            img2 = ImageTk.PhotoImage(img2.resize((image_resize_by_button_H,image_resize_by_button_W)))

            if direction == "up" or direction == "down":
                if image_x == 0:
                    image_x = canvasHeight/2 - image_resize_by_button_H/2
                canvas.create_image(image_x, image_y, anchor='nw', image=img2)
            if direction == "left" or direction == "right":
                if image_y == 0:
                    image_y = canvasWidth/2 - image_resize_by_button_W/2
                canvas.create_image(image_x, image_y, anchor='nw', image=img2)

            # don't delete this even though there are show error  below terminal
            img3 = Image.open("tshirt.pg")
            img3 = ImageTk.PhotoImage(img3)
            canvas.create_image(50, 50, anchor='nw', image=img3)
            # don't delete this


            canvas.pack()

def GButton_go_up_command():
    move("up")

def GButton_go_down_command():
    move("down")

def GButton_go_left_command():
    move("left")

def GButton_go_right_command():
    move("right")

    


# Title
GLabel_Title=tk.Label(root)
ft_title = tkFont.Font(family='Times',size=22)
GLabel_Title["font"] = ft_title
GLabel_Title["fg"] = "#333333"
GLabel_Title["justify"] = "center"
GLabel_Title["text"] = "AI image conversion application"
GLabel_Title.place(x=0,y=10,width=1000,height=60)


ft = tkFont.Font(family='Times',size=15)

GButton_ChooseImage=tk.Button(root,command= GButton_ChooseImage_command) # func GButton_ChooseImage_command will run while onclick a button
GButton_ChooseImage["bg"] = "#f0f0f0"
GButton_ChooseImage["font"] = ft
GButton_ChooseImage["fg"] = "#000000"
GButton_ChooseImage["justify"] = "center"
GButton_ChooseImage["text"] = "Choose image"
GButton_ChooseImage.place(x=30,y=100,width=130,height=30)

GButton_Generate=tk.Button(root,command= GButton_Generate_command) # func GButton_Generate_command will run while onclick a button
GButton_Generate["bg"] = "#f0f0f0"
GButton_Generate["font"] = ft
GButton_Generate["fg"] = "#000000"
GButton_Generate["justify"] = "center"
GButton_Generate["text"] = "Generate"
GButton_Generate.place(x=30,y=140,width=130,height=30)





Radio1 = tk.Radiobutton(root, text="T-Shirt", variable=var, value="1",command= GRadio_1_command) # func GRadio_1_command will run while onclick a radiobutton
Radio1["font"] = ft 
Radio1.place(x=30,y=220,width=130,height=30)

Radio3 = tk.Radiobutton(root, text="Hoodie", variable=var, value="3",command= GRadio_3_command) # func GRadio_3_command will run while onclick a radiobutton
Radio3["font"] = ft
Radio3.place(x=30,y=260,width=130,height=30)

Radio2 = tk.Radiobutton(root, text="None", variable=var, value="0",command= GRadio_2_command) # func GRadio_2_command will run while onclick a radiobutton
Radio2["font"] = ft
Radio2.place(x=30,y=300,width=130,height=30)


GLabel_resize=tk.Label(root)
GLabel_resize["font"] = ft
GLabel_resize["fg"] = "#333333"
GLabel_resize["justify"] = "center"
GLabel_resize["text"] = "Resize :"
GLabel_resize.place(x=30,y=340,width=130,height=30)


button_plus=tk.Button(root,command= GButton_plus_command) # func GButton_plus_command will run while onclick a button + 
button_plus["bg"] = "#f0f0f0"
button_plus["font"] = ft
button_plus["fg"] = "#000000"
button_plus["justify"] = "center"
button_plus["text"] = "+"
button_plus.place(x=55,y=380,width=30,height=30)

button_minus=tk.Button(root,command= GButton_minus_command) # func GButton_minus_command will run while onclick a button -
button_minus["bg"] = "#f0f0f0"
button_minus["font"] = ft
button_minus["fg"] = "#000000"
button_minus["justify"] = "center"
button_minus["text"] = "-"
button_minus.place(x=100,y=380,width=30,height=30)

GButton_SaveImage=tk.Button(root,command= GButton_SaveImage_command) # func GButton_SaveImage_command will run while onclick a button -
GButton_SaveImage["bg"] = "#f0f0f0"
GButton_SaveImage["font"] = ft
GButton_SaveImage["fg"] = "#000000"
GButton_SaveImage["justify"] = "center"
GButton_SaveImage["text"] = "Save image"
GButton_SaveImage.place(x=30,y=180,width=130,height=30)

GLabel_move=tk.Label(root)
GLabel_move["font"] = ft
GLabel_move["fg"] = "#333333"
GLabel_move["justify"] = "center"
GLabel_move["text"] = "Move :"
GLabel_move.place(x=30,y=430,width=130,height=30)


button_go_up=tk.Button(root,command= GButton_go_up_command) # func GButton_plus_command will run while onclick a button + 
button_go_up["bg"] = "#f0f0f0"
button_go_up["font"] = ft
button_go_up["fg"] = "#000000"
button_go_up["justify"] = "center"
button_go_up["text"] = "↑"
button_go_up.place(x=80,y=470,width=30,height=30)

button_go_down=tk.Button(root,command= GButton_go_down_command) # func GButton_plus_command will run while onclick a button + 
button_go_down["bg"] = "#f0f0f0"
button_go_down["font"] = ft
button_go_down["fg"] = "#000000"
button_go_down["justify"] = "center"
button_go_down["text"] = "↓"
button_go_down.place(x=80,y=510,width=30,height=30)


button_go_left=tk.Button(root,command= GButton_go_left_command) # func GButton_plus_command will run while onclick a button + 
button_go_left["bg"] = "#f0f0f0"
button_go_left["font"] = ft
button_go_left["fg"] = "#000000"
button_go_left["justify"] = "center"
button_go_left["text"] = "←"
button_go_left.place(x=40,y=490,width=30,height=30)

button_go_right=tk.Button(root,command= GButton_go_right_command) # func GButton_plus_command will run while onclick a button + 
button_go_right["bg"] = "#f0f0f0"
button_go_right["font"] = ft
button_go_right["fg"] = "#000000"
button_go_right["justify"] = "center"
button_go_right["text"] = "→"
button_go_right.place(x=120,y=490,width=30,height=30)


root.mainloop()