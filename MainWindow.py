from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

from Contrast import make_contrast


def get_img_size(img: Image):
    width, height = img.size
    if width > height:
        height = int(height / width * 375)
        width = 375
    else:
        width = int(width / height * 375)
        height = 375
    return [width, height]


class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title("Контур изображения")
        self.window.geometry("800x600")
        self.window.resizable(0, 0)

        choose_btn = Button(self.window, text="Выбрать изображение", command=self.get_image)
        choose_btn.grid(column=0, row=0, pady=10, padx=[10, 5], sticky="w")
        start_btn = Button(self.window, text="Получить изображение", command=self.get_new_image)
        start_btn.grid(column=1, row=0, pady=10, padx=[5, 10], sticky="w")

        self.image_input = None
        self.photo_input = None

        self.canvas_input = Canvas(self.window, height=375, width=375)
        self.canvas_image_input = None
        self.canvas_input.grid(column=0, row=1, padx=[10, 5])

        self.image_output = None
        self.photo_output = None

        self.canvas_output = Canvas(self.window, height=375, width=375)
        self.canvas_image_output = None
        self.canvas_output.grid(column=1, row=1, padx=[5, 10])

        self.value = IntVar()
        self.value.set(0)
        linear_r = Radiobutton(text='Линейные маски', variable=self.value, value=0)
        gradient_r = Radiobutton(text='Градиентные маски', variable=self.value, value=1)
        laplace_r = Radiobutton(text='Оператор Лапласа', variable=self.value, value=2)
        roberts_r = Radiobutton(text='Оператор Робертса', variable=self.value, value=3)
        prewitt_r = Radiobutton(text='Оператор Превитта', variable=self.value, value=4)
        sobel_r = Radiobutton(text='Оператор Собела', variable=self.value, value=5)
        kirsch_r = Radiobutton(text='Оператор Кирша', variable=self.value, value=6)

        linear_r.grid(column=0, row=2, pady=10, sticky="w")
        gradient_r.grid(column=0, row=3, pady=10, sticky="w")
        laplace_r.grid(column=0, row=4, pady=10,  sticky="w")
        roberts_r.grid(column=1, row=2, pady=10, sticky="w")
        prewitt_r.grid(column=1, row=3, pady=10,  sticky="w")
        sobel_r.grid(column=1, row=4, pady=10, sticky="w")
        kirsch_r.grid(column=1, row=5, pady=10,  sticky="w")

        self.window.mainloop()

    def get_image(self):
        file = filedialog.askopenfilename(filetypes=[("images", ".png .pcx .bmp .jpg")])
        try:
            self.image_input = Image.open(file)
            size = get_img_size(self.image_input)
            self.image_input = self.image_input.resize((size[0], size[1]), Image.ANTIALIAS)
            self.photo_input = ImageTk.PhotoImage(self.image_input)
            self.canvas_image_input = self.canvas_input.create_image(0, 0, anchor='nw', image=self.photo_input)
        except:
            pass

    def get_new_image(self):
        try:
            self.image_output = make_contrast(self.image_input, self.value.get())
            size = get_img_size(self.image_output)
            self.image_output = self.image_output.resize((size[0], size[1]), Image.ANTIALIAS)
            self.photo_output = ImageTk.PhotoImage(self.image_output)
            self.canvas_image_output = self.canvas_output.create_image(0, 0, anchor='nw', image=self.photo_output)
        except:
            pass
