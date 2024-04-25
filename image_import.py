import customtkinter as ctk
from tkinter import filedialog, Canvas


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.import_func = import_func
        ctk.CTkButton(self, text='Open Image', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)


class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, background='#242424', bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=0, column=1, sticky="nsew")
        self.bind('<Configure>', resize_image)

