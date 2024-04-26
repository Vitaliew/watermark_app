import customtkinter as ctk
from tkinter import filedialog

class SidePanel(ctk.CTkFrame):
    def __init__(self, parent, manipulate_image, save_img):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.buttons_frame = ctk.CTkFrame(master=self)

        self.entry_msg = ctk.CTkEntry(self.buttons_frame, placeholder_text="Text")
        self.entry_msg.grid(column=1, row=0, columnspan=3)

        self.entry_r = ctk.CTkEntry(self.buttons_frame, placeholder_text="R", width=45)
        self.entry_g = ctk.CTkEntry(self.buttons_frame, placeholder_text="G", width=45)
        self.entry_b = ctk.CTkEntry(self.buttons_frame, placeholder_text="B", width=45)

        self.entry_r.grid(column=1, row=1, sticky="w")
        self.entry_g.grid(column=2, row=1, sticky="w")
        self.entry_b.grid(column=3, row=1, sticky="w")

        self.size = ctk.CTkEntry(self.buttons_frame, placeholder_text="Size")
        self.size.grid(column=1, row=2, columnspan=3)

        self.opacity_label = ctk.CTkLabel(self.buttons_frame, text="Opacity")
        self.opacity_label.grid(column=1, row=4, columnspan=3)
        self.opacity = ctk.CTkSlider(self.buttons_frame, from_=0, to=255, width=125)
        self.opacity.grid(column=1, row=5, columnspan=3)

        self.angle_label = ctk.CTkLabel(self.buttons_frame, text="Angle")
        self.angle_label.grid(column=1, row=6, columnspan=3)
        self.angle = ctk.CTkSlider(self.buttons_frame, from_=-180, to=180, width=125)
        self.angle.grid(column=1, row=7, columnspan=3)

        self.entry_button = ctk.CTkButton(self.buttons_frame, text='Add Text', command=manipulate_image)
        self.entry_button.grid(column=1, row=10, columnspan=3)

        self.warning = ctk.CTkLabel(self.buttons_frame, text="Fill all boxes!",
                                    text_color="red")
        self.save_button = ctk.CTkButton(self.buttons_frame, text='Save', command=save_img, fg_color="green", hover_color="darkgreen")

        self.buttons_frame.pack(expand=True)

    def get_entry_msg(self):
        # if (self.entry_r.get() == '' or self.entry_g.get() == '' or self.entry_b.get() == ''
        #         or self.entry_msg.get() == '' or self.size.get() == ''):
        if not (self.entry_r.get() or self.entry_g.get() or self.entry_b.get()
                or self.entry_msg.get() or self.size.get()):
            self.warning.grid(column=1, row=11, columnspan=3)
            self.save_button.grid_forget()
        elif (self.entry_r.get().isdigit() is False or self.entry_g.get().isdigit() is False or
              self.entry_b.get().isdigit() is False or self.size.get().isdigit() is False or self.entry_msg.get().isspace()):
            self.warning.configure(text="Use proper values!")
            self.warning.grid(column=1, row=11, columnspan=3)
            self.save_button.grid_forget()
        else:
            self.warning.grid_forget()
            watermark_dict = {
                "R": self.entry_r.get(),
                "G": self.entry_g.get(),
                "B": self.entry_b.get(),
                "opacity": self.opacity.get(),
                "angle": self.angle.get(),
                "size": self.size.get(),
                "msg": self.entry_msg.get()
            }
            self.save_button.grid(column=1, row=12, columnspan=3)
            return watermark_dict


