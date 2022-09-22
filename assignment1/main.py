import tkinter as tk
from tkinter.constants import LEFT, RIGHT
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AIP_40675028H")
        self.geometry("600x400")
        self.btn_load = tk.Button(self,
                                  text="LOAD",
                                  width=4,
                                  height=2,
                                  command=self.load_img)
        self.btn_load.place(x=272, y=160)

        self.btn_save = tk.Button(self,
                                  text="SAVE",
                                  width=4,
                                  height=2,
                                  command=self.save_img)
        self.btn_save.place(x=272, y=200)

        self.btn_exit = tk.Button(self,
                                  text="Exit",
                                  width=4,
                                  height=2,
                                  command=self.destroy)
        self.btn_exit.place(x=272, y=240)

        self.lbl_input = tk.Label(self, text="Input", compound=tk.TOP)
        self.lbl_output = tk.Label(self, text="Output", compound=tk.TOP)

        self.input_img = None
        self.output_img = None

    def save_img(self):
        files = [('All Files', '*.*'), ('JPG', '*.jpg'), ('BMP', '*.bmp'),
                 ("PPM", "*.ppm")]
        file = asksaveasfilename(filetypes=files, defaultextension=files)
        if file:
            self.output_img.save(file)

    def load_img(self):
        files = [('All Files', '*.*'), ('JPG', '*.jpg'), ('BMP', '*.bmp'),
                 ("PPM", "*.ppm")]
        file = askopenfilename(filetypes=files, defaultextension=files)
        img = Image.open(file)

        self.input_img = img

        resized_img = self.input_img.resize((250, 300))
        tkimg_input = ImageTk.PhotoImage(resized_img)
        self.lbl_input.configure(image=tkimg_input)
        self.lbl_input.image = tkimg_input
        self.lbl_input.pack(side=LEFT)

        # do something #
        output_saved = resized_img.resize((self.input_img.size[0], self.input_img.size[1]))
        self.output_img = output_saved
        
        tkimg_ouput = ImageTk.PhotoImage(resized_img)
        self.lbl_output.configure(image=tkimg_ouput)
        self.lbl_output.image = tkimg_ouput
        self.lbl_output.pack(side=RIGHT)


if __name__ == "__main__":
    app = App()
    app.mainloop()