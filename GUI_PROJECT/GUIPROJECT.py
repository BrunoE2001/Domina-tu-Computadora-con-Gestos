import tkinter as tk
from tkinter import PhotoImage, ttk

from Metodos import *


class GUIPROJECT(object):
    def __init__(self):
        root = tk.Tk()
        root.title("Gesture Control")
        root.iconbitmap('img/lenguaje-de-señas.ico')
        root.option_add("*tearOff", False) # quita el separador ---
        root.geometry("400x620")
        root.resizable(False,False)

        root.columnconfigure(index=0, weight=1)
        root.columnconfigure(index=1, weight=1)
        root.columnconfigure(index=2, weight=1)
        root.rowconfigure(index=0, weight=1)
        root.rowconfigure(index=1, weight=1)
        root.rowconfigure(index=2, weight=1)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5)) # Create a style
        style = ttk.Style(root)

        self.widgets_frame = ttk.Frame(root, padding=(20,0, 0, 10))
        self.widgets_frame.grid(row=0, column=0, padx=40, pady=(40,10), sticky="nsew", rowspan=3)
        self.widgets_frame.columnconfigure(index=0, weight=1)

        # Import the tcl file
        root.tk.call("source", "proxttk-dark.tcl")

        # Set the theme with the theme_use method
        style.theme_use("proxttk-dark")

        self.metodos = Metodos()
        self.ventana()

        root.mainloop()

    def ventana(self):
        d = tk.IntVar(value=2)

        # Label
        title = ttk.Label(self.widgets_frame, text="GRAPHING PROJECT",font="colortube 20",foreground="white")
        title.grid(row=0, column=1, pady=10, columnspan=2)

        img = PhotoImage(file="img/lenguaje-de-senas.png")
        text1 = ttk.Label(self.widgets_frame, image=img)
        text1.grid(row=1, column=1, pady=10, columnspan=2)

        d = tk.IntVar(value=2)
        #  read images
        imgvolumen = PhotoImage(file="img/bajo-volumen.png")
        imgraton   = PhotoImage(file="img/raton.png")
        imgbrillo  = PhotoImage(file="img/brillo.png")
        imgwindow  = PhotoImage(file="img/sistema-operativo.png")
        imgface    = PhotoImage(file="img/facial-recognition.png")
        imgcls     = PhotoImage(file="img/procesamiento-de-imagenes.png")

        # Botones
        btnvolumen = ttk.Button(self.widgets_frame, text="Control Volume", image = imgvolumen, style="AccentButton", command= self.metodos.volumen)
        btnvolumen.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        btnmouse = ttk.Button(self.widgets_frame, text="Mouse Control", image = imgraton, style="AccentButton", command= self.metodos.mousevirtual)
        btnmouse.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

        btnbrillo = ttk.Button(self.widgets_frame, text="Brightness control", image = imgbrillo, style="AccentButton", command= self.metodos.brillo)
        btnbrillo.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        btnwindows = ttk.Button(self.widgets_frame, text="Window Control", image = imgwindow, style="AccentButton")
        btnwindows.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")

        btnFace = ttk.Button(self.widgets_frame, text="Face Detection", image = imgface, style="AccentButton")
        btnFace.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        btnImg = ttk.Button(self.widgets_frame, text="image classifier", image = imgcls, style="AccentButton")
        btnImg.grid(row=4, column=2, padx=5, pady=5, sticky="nsew")

if __name__ == '__main__':
    GUIPROJECT()