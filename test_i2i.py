import base64
import io
import os
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image, ImageGrab
from tkinter import CENTER, filedialog  , ttk

import requests

root = tk.Tk()
#setting title
root.title("AI image conversion application")

#setting color
black = "#232931"
white = "#EEEEEE"
dark = "#393E46"
gray = "#8A8A8A"
mint = "#4ECCA3"
red = "#F37777"


#setting window size
root.configure(background=black)
width=1300
height=650
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

#global var
engine_id = "stable-diffusion-v1-5"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = "sk-yxjiu9Sf8g0kpM3NcA86hYeQV9ajxFm7T0QHR0CZ3weYQGLl"
if api_key is None:
    raise Exception("Missing Stability API key.")
file_path_upload = ""
file_path_image_on_shirt = ""
file_path_image_background = ""

file_path_image_generate = ""
image_resize_by_button_H = 100
image_resize_by_button_W = 100

image_x = 0
image_y = 0

flag = False

canvasHeight = 500
canvasWidth = 500
canvas = tk.Canvas(root, width=canvasHeight, height=canvasWidth)
canvas.place(x=550, y=80) 
canvas.configure(background=black, borderwidth=0, highlightthickness=0)

var = tk.IntVar()

style = "none"

#global var
separatorV = tk.Frame(width=1, background=dark )
separatorV.place(x=300, y=0)
separatorV.pack(side='left',fill="y",padx=300)


def upload_image(file_path):

    def button_delete_command():
        GButton_Upload["text"] = "Upload image"
        global file_path_upload
        file_path_upload = ""
        window.destroy()

    image = Image.open(file_path)
            
    # Resize the image using resize() method
    imgH = 400
    imgW = 400
    resize_image = image.resize((imgW, imgH))
            
    img = ImageTk.PhotoImage(resize_image)
            
    # create label and add resize image
    # label1 = self.GLabel(image=img)

    

    window = tk.Toplevel(root,width=410, height=410)
    window.geometry("+150+110")
    window.title("View Image")
    window.resizable(width=False, height=False)
    window.attributes('-topmost', 1)
    window.configure(background=black)

    label_image = tk.Label(window,image=img)
    label_image.image = img
    label_image.place(x=5,y=5,width=imgW,height=imgH)

    # Button delete
    path = "images/delete.png"
                
    # open the image file and resize it
    img = Image.open(path)
    img = img.resize((25, 25))
                
    # create a photo image object from the resized image
    photo_img = ImageTk.PhotoImage(img)
    ft = tkFont.Font(family='Times',size=15)
    GButton_Upload["text"] = "View image"
    # create a button with the photo image and place it on the grid
    button_delete = tk.Button(window, image=photo_img, compound="center", borderwidth=0, relief="flat",width=30,height=30,command=button_delete_command)
    button_delete["font"] = ft
    button_delete["fg"] = white
    button_delete.image = photo_img
    button_delete.configure(background=red)
    button_delete.place(x=0,y=0)
    # Button delete

def GButton_ChooseImage_command():
    global file_path_upload
    # Choose file by dialog
    if file_path_upload == "":
        file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.png;*.jpg"), ("All files", "*.*")))
        file_path_upload = file_path
        # open an image file 
        upload_image(file_path)
    
    else:
        upload_image(file_path_upload)
    
def GButton_Generate_command():

    global flag 
    flag = False
    
    positivePrompt = textPrompt.get(1.0, "end-1c")
    negativePrompt = textPromptNegative.get(1.0, "end-1c")
    style = GButton_Style.cget("text")
    result = ""

    if file_path_upload != "":
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/image-to-image",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            files={
                "init_image": open(file_path_upload, "rb")
            },
            data={
                "image_strength": 1.0,
                "init_image_mode": "IMAGE_STRENGTH",
                "text_prompts[0][text]": "bird",
                "cfg_scale": 20,
                "clip_guidance_preset": "FAST_BLUE",
                "samples": 1,
                "steps": 50,
            }
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))
        
        data = response.json()
        
        image_data = data["artifacts"][0]["base64"]

        # decode the base64 image data
        decoded_image_data = base64.b64decode(image_data)
        print("i2i")
        

    if positivePrompt != "":
        if negativePrompt != "":
            for item in negativePrompt.split(","):
                result += item + ":-1,"
            result = result[:-1]   # remove the extra comma at the end
                
        if style == "Style" or style == "none":
            style = ""
        else:
            style = "," + style
            
        prompt = positivePrompt + "," + style + "," + result
            
            
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "clip_guidance_preset": "FAST_BLUE",
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 30,
            },
        )
        
        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
            
        image_data = data["artifacts"][0]["base64"]

        # decode the base64 image data
        decoded_image_data = base64.b64decode(image_data)
        print("t2i")
        
            
    global file_path_image_on_shirt 
    file_path_image_on_shirt = io.BytesIO(decoded_image_data)
        
    imgH = 350
    imgW = 350
    img1 = Image.open(file_path_image_on_shirt)
        
    # Create ImageTk.PhotoImage object from resized image
    img1 = ImageTk.PhotoImage(img1.resize((canvasHeight,canvasWidth)))

    canvas.create_image(0, 0, anchor='nw', image=img1)

    # don't delete this
    # img3 = Image.open("tshirt.pg")
    # img3 = ImageTk.PhotoImage(img3)
    canvas.create_image(50, 50, anchor='nw', image=img3)
    # don't delete this

    canvas.pack()
        
    
def GRadio_1_command():
    global flag 
    flag = True
    # delete old image available on canvas 
    canvas.delete("all")

    # open the background image
    path = os.path.join(os.path.dirname(__file__), "images/T-Shirt_1.png")
    img1 = Image.open(path)
    img1 = ImageTk.PhotoImage(img1.resize((canvasHeight,canvasWidth)))

    # add image to canvas
    canvas.create_image(0, 0, anchor='nw', image=img1)

    # use api image to set on image
    global file_path_image_background

    # define global image by path
    # because the func resize by button need to load the background again
    file_path_image_background = path

    # open the api image
    # add image to canvas
    global file_path_image_on_shirt
    
    #path2 = os.path.join(os.path.dirname(__file__), "images/2.png")
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
    
    global file_path_image_on_shirt
    img1 = Image.open(file_path_image_on_shirt)
    img1 = ImageTk.PhotoImage(img1.resize((canvasHeight,canvasWidth)))
    
    canvas.delete("all")
    
    canvas.create_image(0, 0, anchor='nw', image=img1)

    # don't delete this
    img3 = Image.open("tshirt.pg")
    img3 = ImageTk.PhotoImage(img3)
    canvas.create_image(50, 50, anchor='nw', image=img3)
    # don't delete this

    canvas.pack()

def GRadio_3_command():
    global flag 
    flag = True
    # this func the same of the GRadio_1_command
    canvas.delete("all")
    #path = "hoodie.jpg"
    path = os.path.join(os.path.dirname(__file__), "images/hoodie.jpg")
    img1 = Image.open(path)
    img1 = ImageTk.PhotoImage(img1.resize((canvasHeight,canvasWidth)))
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
                if image_resize_by_button_H < canvasHeight - 310 and image_resize_by_button_W < canvasWidth - 310:

                    # plus 5px (width,height) while click on button +
                    image_resize_by_button_H += 5
                    image_resize_by_button_W += 5

            if scale == "minus":
                if image_resize_by_button_H > 30 and image_resize_by_button_W > 30:
                    image_resize_by_button_H -= 5
                    image_resize_by_button_W -= 5

            # and reload all image include background
            global file_path_image_background
            img1 = Image.open(file_path_image_background)
            img1 = ImageTk.PhotoImage(img1.resize((canvasHeight,canvasWidth)))
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
                if image_y < (canvasHeight - image_resize_by_button_H - 10):
                    image_y += 5
            if direction == "left":
                if image_x > 50:
                    image_x -= 5
            if direction == "right":
                if image_x < (canvasWidth - image_resize_by_button_W - 135):
                    image_x += 5
            global file_path_image_background
            img1 = Image.open(file_path_image_background)
            img1 = ImageTk.PhotoImage(img1.resize((canvasHeight,canvasWidth)))
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


def create_window():

    # create a new window and set its title
    window = tk.Toplevel(root,width=500, height=500)
    window.geometry("+520+240")
    window.title("Choose style")
    window.resizable(width=False, height=False)
    window.attributes('-topmost', 1)
    window.configure(background=black)

    canvasButtonFrame = tk.Canvas(window,width=430,height=500)
    canvasButtonFrame.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(window, command=canvasButtonFrame.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    canvasButtonFrame.configure(yscrollcommand=scrollbar.set)
    canvasButtonFrame.bind('<Configure>', lambda e: canvasButtonFrame.configure(scrollregion = canvasButtonFrame.bbox('all')))

    button_frame = tk.Frame(canvasButtonFrame)
    button_frame.configure(background=black)
    button_frame.pack()

    canvasButtonFrame.create_window((0,0), window=button_frame, anchor = 'nw')
    
    # func to close choose style
    def choose_style(button):
        global style
        style = button.cget('text')
        #print(style)
        GButton_Style["text"] = style
        window.destroy()

    #define style
    dictStyle = {
        0: "none",
        1: "enchance",
        2: "anime",
        3: "photographic",
        4: "digital art",
        5: "comic book",
        6: "fantasy art",
        7: "analog film",
        8: "neon punk",
        9: "isometric",
        10: "low poly",
        11: "origami",
        12: "line art",
        13: "craft clay",
        14: "cinematic",
        15: "3d model",
        16: "pixel art"
    }
    
    # create the buttons and add them to the frame
    for row in range(6):
        for col in range(3):
            # construct the path to the image file
            if row * 3 + col < 17:
                tempImageIndex =str(row * 3 + col) + ".png"
                
                path = os.path.join(os.path.dirname(__file__), "images/" + tempImageIndex)
                
                # open the image file and resize it
                img = Image.open(path)
                img = img.resize((130, 130))
                
                # create a photo image object from the resized image
                photo_img = ImageTk.PhotoImage(img)
                ft = tkFont.Font(family='Times',size=15)
                # create a button with the photo image and place it on the grid
                button = tk.Button(button_frame, text=dictStyle[row * 3 + col], image=photo_img, compound="top", borderwidth=0)
                button["font"] = ft
                button["fg"] = white
                button.image = photo_img
                button.configure(background=black)
                button.grid(row=row, column=col, padx=5, pady=5)
                
                button.config(command=lambda btn=button: choose_style(btn))


#---------------GUI--------------------------------------------------------------------------------------
# Title
GLabel_Title=tk.Label(root)
ft_title = tkFont.Font(family='Times',size=18)
GLabel_Title["font"] = ft_title
GLabel_Title["fg"] = white
GLabel_Title["bg"]  = black
GLabel_Title["justify"] = "left"
GLabel_Title["text"] = "AI image conversion application"
GLabel_Title.place(x=10,y=0,height=35)
# Title

# Seperate line
separatorH = tk.Frame(width = 1500,height=1, background=dark)
separatorH.place(x=0, y=35) 
# Seperate line



# Font 
ft = tkFont.Font(family='Times',size=15)
ft_small_label = tkFont.Font(family='Times',size=13)
# Font 


# Label Style
GLabel_Style=tk.Label(root)
GLabel_Style["bg"] = black
GLabel_Style["font"] = ft_small_label
GLabel_Style["fg"] = gray
GLabel_Style["text"] = "Style"
GLabel_Style.place(x=10,y=40,height=25)
# Label Style


# Button Style
GButton_Style=tk.Button(root,command= create_window,relief="flat", borderwidth=1,highlightthickness=2) 
GButton_Style["bg"] = dark
GButton_Style["font"] = ft
GButton_Style["fg"] = white
GButton_Style["justify"] = "left"
GButton_Style["text"] = "Style"
GButton_Style.place(x=10,y=70,width=280,height=35)
# Button Style


# Seperate line
separatorH1 = tk.Frame(width = 300,height=1, background=dark)
separatorH1.place(x=0, y=115) 
# Seperate line

# Label Image
GLabel_Image=tk.Label(root)
GLabel_Image["bg"] = black
GLabel_Image["font"] = ft_small_label
GLabel_Image["fg"] = gray
GLabel_Image["text"] = "Image"
GLabel_Image.place(x=10,y=120,height=25)
# Label Image


# Button Upload
GButton_Upload=tk.Button(root,command= GButton_ChooseImage_command,relief="flat", borderwidth=1,highlightthickness=2) 
GButton_Upload["bg"] = dark
GButton_Upload["font"] = ft
GButton_Upload["fg"] = white
GButton_Upload["justify"] = "left"
GButton_Upload["text"] = "Upload image"
GButton_Upload.place(x=10,y=150,width=280,height=35)
# Button Upload



# Seperate line
separatorH2 = tk.Frame(width = 300,height=1, background=dark)
separatorH2.place(x=0, y=199)
# Seperate line

#Prompt label
GLabel_Prompt = tk.Label(root)
GLabel_Prompt["bg"] = black
GLabel_Prompt["font"] = ft_small_label
GLabel_Prompt["fg"] = gray
GLabel_Prompt["text"] = "Prompt"
GLabel_Prompt.place(x=10, y=200,height=25)

#Text promt
textPrompt = tk.Text(root, font="family='Helvetica', 12", height=3)
textPrompt.place(x=10, y=230, width=280, height=65)


#Negative Prompt label
GLabel_Negative = tk.Label(root)
GLabel_Negative["bg"] = black
GLabel_Negative["font"] = ft_small_label
GLabel_Negative["fg"] = gray
GLabel_Negative["text"] = "Negative Prompt"
GLabel_Negative.place(x=10, y=305,height=25)

#Text promt for negative
textPromptNegative = tk.Text(root, font="family='Helvetica', 12", height=3)
textPromptNegative.place(x=10, y=335, width=280, height=65)


# Seperate line
separatorH3 = tk.Frame(width = 300,height=1, background=dark)
separatorH3.place(x=0, y=410) 
# Seperate line

# Button Generate
GButton_Generate=tk.Button(root,command= GButton_Generate_command,relief="flat", borderwidth=1,highlightthickness=2) 
GButton_Generate["bg"] = mint
GButton_Generate["font"] = ft
GButton_Generate["fg"] = dark
GButton_Generate["justify"] = "left"
GButton_Generate["text"] = "Generate image"
GButton_Generate.place(x=10,y=420,width=280,height=35)
# Button Generate


# Seperate line
separatorH4 = tk.Frame(width = 300,height=1, background=dark)
separatorH4.place(x=0, y=465) 
# Seperate line


# Label Type
GLabel_Type=tk.Label(root)
GLabel_Type["bg"] = black
GLabel_Type["font"] = ft_small_label
GLabel_Type["fg"] = gray
GLabel_Type["text"] = "Type"
GLabel_Type.place(x=10,y=470,height=25)
# Label Type


# Radio button T-Shirt
Radio1 = tk.Radiobutton(root, text="T-Shirt", variable=var, value="1",command= GRadio_1_command, background=black) # func GRadio_1_command will run while onclick a radiobutton
Radio1["font"] = ft 
Radio1["fg"] = white
Radio1.place(x=10,y=500,height=30)
# Radio button T-Shirt

# Radio button None
Radio2 = tk.Radiobutton(root, text="None", variable=var, value="0",command= GRadio_2_command, background=black) # func GRadio_2_command will run while onclick a radiobutton
Radio2["font"] = ft 
Radio2["fg"] = white
Radio2.place(x=210,y=500,height=30)
# Radio button None

# Seperate line
separatorH5 = tk.Frame(width = 300,height=1, background=dark)
separatorH5.place(x=0, y=535) 
# Seperate line


# Label Resize
GLabel_Resize=tk.Label(root)
GLabel_Resize["bg"] = black
GLabel_Resize["font"] = ft_small_label
GLabel_Resize["fg"] = gray
GLabel_Resize["text"] = "Resize"
GLabel_Resize.place(x=10,y=540,height=25)
# Label Resize

# Button Resize Plus
button_plus=tk.Button(root,command= GButton_plus_command, relief="flat") # func GButton_plus_command will run while onclick a button + 
button_plus["bg"] = dark
button_plus["font"] = ft
button_plus["fg"] = white
button_plus["justify"] = "center"
button_plus["text"] = "+"
button_plus.place(x=20,y=570,width=30,height=30)
# Button Resize Plus


# Button Resize Minus
button_minus=tk.Button(root,command= GButton_minus_command, relief="flat") # func GButton_minus_command will run while onclick a button -
button_minus["bg"] = dark
button_minus["font"] = ft
button_minus["fg"] = white
button_minus["justify"] = "center"
button_minus["text"] = "-"
button_minus.place(x=20,y=610,width=30,height=30)
# Button Resize Minus

separatorV1 = tk.Frame(width=1, height=130, background=dark )
separatorV1.place(x=70, y=535)


# Label Move
GLabel_Move=tk.Label(root)
GLabel_Move["bg"] = black
GLabel_Move["font"] = ft_small_label
GLabel_Move["fg"] = gray
GLabel_Move["text"] = "Move image in side the T-shirt"
GLabel_Move.place(x=80,y=540,height=25)
# Label Move

# Button Move up
button_go_up=tk.Button(root,command= GButton_go_up_command, relief="flat") # func GButton_plus_command will run while onclick a button + 
button_go_up["bg"] = dark
button_go_up["font"] = ft
button_go_up["fg"] = white
button_go_up["justify"] = "center"
button_go_up["text"] = "↑"
button_go_up.place(x=165,y=570,width=30,height=30)
# Button Move up


# Button Move down
button_go_down=tk.Button(root,command= GButton_go_down_command, relief="flat") # func GButton_plus_command will run while onclick a button + 
button_go_down["bg"] = dark
button_go_down["font"] = ft
button_go_down["fg"] = white
button_go_down["justify"] = "center"
button_go_down["text"] = "↓"
button_go_down.place(x=165,y=610,width=30,height=30)
# Button Move down


# Button Move left
button_go_left=tk.Button(root,command= GButton_go_left_command, relief="flat") # func GButton_plus_command will run while onclick a button + 
button_go_left["bg"] = dark
button_go_left["font"] = ft
button_go_left["fg"] = white
button_go_left["justify"] = "center"
button_go_left["text"] = "←"
button_go_left.place(x=125,y=590,width=30,height=30)
# Button Move left


# Button Move right
button_go_right=tk.Button(root,command= GButton_go_right_command, relief="flat") # func GButton_plus_command will run while onclick a button + 
button_go_right["bg"] = dark
button_go_right["font"] = ft
button_go_right["fg"] = white
button_go_right["justify"] = "center"
button_go_right["text"] = "→"
button_go_right.place(x=205,y=590,width=30,height=30)
# Button Move right


# Button Save
GButton_Save=tk.Button(root,command= GButton_SaveImage_command,relief="flat", borderwidth=1,highlightthickness=2) 
GButton_Save["bg"] = dark
GButton_Save["font"] = ft
GButton_Save["fg"] = gray
GButton_Save["justify"] = "left"
GButton_Save["text"] = "Save image"
GButton_Save.place(x=660,y=605,width=280,height=35)
# Button Save


#---------------GUI--------------------------------------------------------------------------------------



root.mainloop()