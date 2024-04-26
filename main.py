import customtkinter as ctk

import photo_manipulation
from image_import import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
from photo_manipulation import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Watermark")
        self.geometry("1000x600")
        self.minsize(800, 500)
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2, uniform="a")
        self.grid_columnconfigure(1, weight=6, uniform="a")
        self.image_height = 0
        self.image_width = 0
        self.canvas_height = 0
        self.canvas_width = 0
        self.rotation = 0

        # The importing image screen
        self.image_import = ImageImport(self, self.import_image)

    def import_image(self, path):
        self.original = Image.open(path).convert("RGBA")
        self.image = self.original
        self.transparent_overlay = Image.new("RGBA", (self.image.width, self.image.height), (0, 0, 0, 0))
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_import.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        # Create the side panel
        self.side_panel = SidePanel(self, self.manipulate_image, self.save_img)

    def resize_image(self, event):
        canvas_ratio = event.width / event.height

        self.canvas_width = event.width
        self.canvas_height = event.height
        # Check the ratio
        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
        self.place_image()

    def place_image(self):
        # Delete the repeating images
        self.image_output.delete('all')
        # Show the image

        # print(self.image.size)
        rotated_transparent_overlay = self.transparent_overlay.rotate(self.rotation)
        resized_image = self.image.resize((self.image_width, self.image_height))
        crop_size = (0,
                     0,
                     int(resized_image.width),
                     int(resized_image.height))
        resized_transparent_overlay = rotated_transparent_overlay.resize((self.image_width * 2, self.image_height * 2))

        # result = Image.alpha_composite(resized_image, self.resized_transparent_overlay)
        offset = ((resized_image.width - resized_transparent_overlay.width) // 2, (resized_image.height - resized_transparent_overlay.height) // 2)
        resized_image.paste(resized_transparent_overlay, offset, resized_transparent_overlay)
        self.result = resized_image
        self.image_tk = ImageTk.PhotoImage(self.result.convert("RGB"))
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

    def manipulate_image(self):

        self.image = self.original
        self.transparent_overlay = Image.new("RGBA", (int(self.image.width), int(self.image.height)), (0, 0, 0, 0))
        self.drawer = ImageDraw.Draw(self.transparent_overlay)
        self.watermark_dict = photo_manipulation.SidePanel.get_entry_msg(self.side_panel)
        if self.watermark_dict:
            r = int(self.watermark_dict['R'])
            g = int(self.watermark_dict['G'])
            b = int(self.watermark_dict['B'])
            msg = self.watermark_dict["msg"]
            opacity = int(self.watermark_dict["opacity"])
            angle = int(self.watermark_dict["angle"])
            size = int(self.watermark_dict["size"])
            font = ImageFont.truetype("arial.ttf", size, encoding="unic")
            width = self.drawer.textlength(msg, font=font)
            self.rotation = angle
            for n in range(0, self.original.height, int(width)):
                x = 0
                y = 0 + n
                for j in range(0, self.original.width, 100):
                    self.drawer.text(((x + j), y), f"{msg}",
                                     fill=(r, g, b, opacity),
                                     font=font)
                    x += int(width)
            self.place_image()

    def save_img(self):
        file = filedialog.asksaveasfilename(filetypes=[("PNG Image", "*.png")])
        # print(file)
        if file:
            self.result.convert("RGB").save(f"{file}.png", 'PNG')


app = App()
app.mainloop()
