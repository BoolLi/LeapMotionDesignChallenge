#!/usr/bin/env python

import matplotlib
#matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Embedding in TK")

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0, 3.0, 0.01)
s = sin(2*pi*t)

a.plot(t, s)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate



label1 = Tk.Label(master=root, text="MinX")
label2 = Tk.Label(master=root, text="MaxX")
label3 = Tk.Label(master=root, text="MinY")
label4 = Tk.Label(master=root, text="MaxY")
label5 = Tk.Label(master=root, text="z(x,y)")


entry1 = Tk.Entry(master=root)
entry2 = Tk.Entry(master=root)
entry3 = Tk.Entry(master=root)
entry4 = Tk.Entry(master=root)
entry5 = Tk.Entry(master=root)


"""
button2 = Tk.Button(master=root, text='Quit', command=_quit)
button2.pack(side=Tk.BOTTOM)
"""

label1.pack()

"""
entry1.pack(side=Tk.LEFT)
label2.pack(side=Tk.LEFT)
entry2.pack(side=Tk.LEFT)

label3.pack(side=Tk.LEFT)
entry3.pack(side=Tk.LEFT)
label4.pack(side=Tk.LEFT)
entry4.pack(side=Tk.LEFT)

label5.pack(side=Tk.BOTTOM)
entry5.pack(side=Tk.BOTTOM)

button1 = Tk.Button(master=root, text='Plot', command=_plotData)
button1.pack(side=Tk.BOTTOM)
"""


def get_function(self):
    return self.entry1.get()

def get_color(self):
	return self.entry2.get()

def get_upper_x(self):
	return self.entry4.get()

def get_lower_x(self):
	return self.entry5.get()

def get_upper_y(self):
	return self.entry6.get()

def get_lower_y(self):
	return self.entry7.get()

def get_speed(self):
	return self.entry3.get()

def _plotData(self):
	infix = self.get_function()
	endX = float(self.get_upper_x())
	beginX = float(self.get_lower_x())
	endY = float(self.get_upper_y())
	beginY = float(self.get_lower_y())

	X = np.linspace(beginX, endX, RESOLUTION)
	Y = np.linspace(beginY, endY, RESOLUTION)
	Z = np.zeros((RESOLUTION,RESOLUTION))

	postfix = translate( infix )

	for i in range(RESOLUTION):
	    for j in range(RESOLUTION):
	        Z[i][j] = transfer_to_postfix( postfix, X[i], Y[j] )

	X,Y = np.meshgrid(X,Y)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap = "Oranges_r", linewidth=0, antialiased=True)
	plt.show()

"""
label1.grid(row=10,column=1)
button1.grid(row=10,column=3)
entry1.grid(row=10,column=2)

label2.grid(row=11,column=1)
button2.grid(row=11,column=3)
entry2.grid(row=11,column=2)


label3.grid(row=22,column=1)
button3.grid(row=22,column=3)
entry3.grid(row=22,column=2)

"""

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
