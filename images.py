from tkinter import *
from PIL import ImageTk, Image
import os
import sqlite3

form = Tk()
form.title('Images')
form.iconbitmap('icon.ico')

images = []
image_index = 0

# to init image (resize image)


def image(path, percent=25, width=500, height=500):
    image = Image.open(path)

    if image.size[0] > width and image.size[1] > height:
        return image.resize((round(image.size[0]*(percent/100)), round(image.size[1]*(percent/100))))
    else:
        return image


def find_images():
    global images
    images_locations = []
    try:
        db = sqlite3.connect("path.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM path")
        values = cursor.fetchall()
        for value in values:
            images_locations.append(value[0])
        db.close()
    except:
        pass
    for images_location in images_locations:
        try:
            if os.path.isfile(images_location):
                images.append(ImageTk.PhotoImage(image(images_location)))
            else:
                for i in os.listdir(images_location):
                    images_locations.append(r'' + images_location + "/" + i)
                    print(r'' + images_location + "/" + i)
        except:
            continue


find_images()

# label, that contains image
try:
    label = Label(image=images[image_index])
except:
    label = Label(text="Выберите местоположение изображений")

label.grid(row=0, column=0, columnspan=3)

try:
    status = Label(text="Image {0} of {1}".format(
        image_index+1, len(images)), bd=1, relief=SUNKEN, anchor=E)
except:
    status = Label(text="It is not images", bd=1, relief=SUNKEN, anchor=E)

status.grid(row=2, column=0, columnspan=3, sticky=W+E)


def change_image(side):
    global label
    global status
    global image_index

    if side == "forward":
        if image_index + 1 <= len(images) - 1:
            image_index += 1
        else:
            image_index = 0

    if side == "back":
        if image_index - 1 >= 0:
            image_index -= 1
        else:
            image_index = len(images) - 1
    if images:
        label.grid_forget()
        label = Label(image=images[image_index])
        label.grid(row=0, column=0, columnspan=3)

        status.grid_forget()
        status = Label(text="Image {0} of {1}".format(
            image_index+1, len(images)), bd=1, relief=SUNKEN, anchor=E)
        status.grid(row=2, column=0, columnspan=3, sticky=W+E)


back_button = Button(text="<<", command=lambda: change_image("back"))
back_button.grid(row=1, column=0, pady=10)

forward_button = Button(text=">>", command=lambda: change_image("forward"))
forward_button.grid(row=1, column=2, pady=10)


def entry_img_location():
    form = Toplevel()
    form.title("Images Location")
    form.iconbitmap("icon.ico")

    def save_img_location(path):
        try:
            db = sqlite3.connect("path.db")
            cursor = db.cursor()
            cursor.execute("INSERT INTO path VALUES (:location)", {
                           'location': path})
            db.commit()
            db.close()
        except:
            pass

    text = Label(form, text="Input images location")
    text.grid(row=0, column=0, columnspan=3, padx=10)

    entry = Entry(form, width=35)
    entry.grid(row=1, column=1, padx=10, pady=10)

    button = Button(form, text="Save",
                    command=lambda: save_img_location(r'' + entry.get()))
    button.grid(row=2, column=1, padx=5, pady=5)

    form.mainloop()


entry_img_location_button = Button(
    text="Images location", command=entry_img_location)
entry_img_location_button.grid(row=1, column=1)

form.mainloop()
