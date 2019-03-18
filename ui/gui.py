# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 20:17:45 2019

@author: Admin
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import tkinter as tk
from tkinter import ttk
from time import sleep

HEADINGS = ("Verdana Black", 18)
btnfont = ("Verdana", 10)
style.use("dark_background")
toggle = False

#Live Animation Stuff
#Defining figure to draw stuff
f = Figure()
a1 = f.add_subplot(121)
a1.set_title("Force Map")
#Loads data from a text file
data = np.loadtxt("junkdata.txt", delimiter=",")
im = a1.imshow(data)
cbar = f.colorbar(im, orientation="horizontal")
cbar.set_clim(vmin=0, vmax=1)

a2 = f.add_subplot(122)
x1 = np.arange(5)
y1 = x1**3
a2.plot(x1, y1)
a2.set_title("Velocity vs Time")
a2.set_xlabel("time (ms)")
a2.set_ylabel("Velocity (mm/ms)")


def getData():
    ####Before David's Changes
    """
    ardata = np.asarray(np.load("ardata.pkl")).reshape(10, 10)
    linedata = np.asarray(np.load("linedata.pkl")).reshape(10, 10)
    """

    ####David's Changes
    ardata = np.asarray(np.load("ardata.pkl"))
    linedata = np.asarray(np.load("linedata.pkl"))
    ####End David's Changes

    return ardata, linedata


def animate(i):
    ardata, linedata = getData()

    ####Before David's Changes
    """
    #Array data
    a1.clear()
    a1.set_xticks(np.arange(0, 10))
    a1.set_yticks(np.arange(0, 10))
    a1.set_title("Force Map")
    im = a1.imshow(ardata)
    cbar.update_bruteforce(im)

    #Line data
    a2.clear()
    a2.plot(linedata[0], linedata[1])
    """

    ####David's Changes
    colourbarset = 0.1  #I will add this thing to the data so it stabilizes. This needs to be chosen correctly
    polydeg = 4

    sumx = ardata[0:10]
    sumy = ardata[10:]

    course_spacing = np.arange(10)

    polyx = np.polyfit(course_spacing, sumx, polydeg)
    polyy = np.polyfit(course_spacing, sumy, polydeg)

    fine_spacing = np.arange(0, 9.1, 0.1)
    len_fine_spacing = len(fine_spacing)

    polyX = np.polyval(polyx, fine_spacing)
    polyY = np.polyval(polyy, fine_spacing)

    NEWardata = np.ones(
        (len_fine_spacing + 2, len_fine_spacing + 2)) * colourbarset

    for i in range(0, len_fine_spacing):
        for j in range(0, len_fine_spacing):
            NEWardata[i + 1][j + 1] = polyX[i]

    for i in range(0, len_fine_spacing):
        for j in range(0, len_fine_spacing):
            NEWardata[i + 1][j + 1] += polyY[j]

    #Array data
    a1.clear()
    a1.set_xticks(np.arange(1, len_fine_spacing + 1, 10))
    a1.set_yticks(np.arange(1, len_fine_spacing + 1, 10))
    a1.set_xticklabels(np.arange(10))
    a1.set_yticklabels(np.arange(10))
    a1.set_title("Force Map")
    im = a1.imshow(NEWardata)
    cbar.update_bruteforce(im)

    #Line data
    #Can replace this plot with sumx, sumy, polyX and polyY for debugging
    FFTDATA = abs(np.fft.fft(linedata))
    FFTxaxis = np.arange(len(FFTDATA))
    a2.clear()
    a2.plot(FFTxaxis, FFTDATA)

    #a2.plot(fine_spacing, polyX)
    #a2.plot(course_spacing, sumx)
    #a2.plot(fine_spacing, polyY)
    #a2.plot(course_spacing, sumy)
    ####End David's Changes


class FYDPGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        "This runs every time the function is initialized"
        tk.Tk.__init__(self, *args, **kwargs)

        #Adding icon
        # tk.Tk.iconbitmap(self, "FYDPIcon.ico")
        tk.Tk.wm_title(self, "Sensor Dashboard")

        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid(row=0, column=0, sticky=tk.S + tk.N + tk.E + tk.W)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, GraphPage):
            frame = F(container, self)
            #In this case, container is passed as the parent
            #and self (FYDPGUI) is passed as the controller

            self.frames[F] = frame

            #Aligning frame
            #Frame is part of the container
            frame.grid(row=0, column=0, sticky="nsew")
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)

        self.show_frame(GraphPage)
        self.config(bg="red")

    def show_frame(self, page):
        "Brings the 'page' to the front so we can see it"
        frame = self.frames[page]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=HEADINGS)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(
            self,
            text="Visit Page 1",
            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(
            self,
            text="Visit Page 2",
            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(
            self,
            text="Visit Graph Page",
            command=lambda: controller.show_frame(GraphPage))
        button3.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(0, weight=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        label = tk.Label(self, text="Page One", font=HEADINGS)
        label.grid(row=0, column=0)

        button1 = ttk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two", font=HEADINGS)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(
            self,
            text="Page One",
            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="black")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        label = tk.Label(
            self,
            text="Graph Page",
            font=HEADINGS,
            bg="black",
            fg="white",
            pady=20)
        label.grid(row=0, column=0, columnspan=3, sticky=tk.E + tk.W)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().grid(
            row=1, column=0, columnspan=3, sticky=tk.E + tk.W + tk.N + tk.S)
        canvas.draw()

        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=3, column=0, columnspan=3, sticky=tk.N + tk.W)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

        #        canvas._tkcanvas.grid(row=10, column=2, columnspan=2)
        def pause():
            global toggle
            toggle ^= True
            if toggle:
                ani.event_source.stop()
                #setting background color
                global pausebutton
                pausebutton.config(
                    background="darkorchid4", text="Play", relief=tk.SUNKEN)

            else:
                ani.event_source.start()
                pausebutton.config(
                    background="darkorchid3", text="Pause", relief=tk.RAISED)

        global pausebutton
        pausebutton = tk.Button(
            self,
            text="Pause",
            command=pause,
            bg="darkorchid3",
            font=btnfont,
            fg="white")
        pausebutton.grid(row=2, column=1, sticky=tk.E + tk.W)


app = FYDPGUI()
ani = animation.FuncAnimation(f, animate, interval=10)
app.mainloop()
