import Tkinter
from Tkinter import *
from infix2postfix import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

RESOLUTION = 20

class Demo(Tkinter.Tk):
    def __init__(self):
        # X, Y, Z
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.hasData = False
        self.var= "Blues"
        self.colorVal = "Blues"

        # GUI
        Tkinter.Tk.__init__(self)
        self.title("ESCALA 1.0")

        #MinX
        self.label1 = Tkinter.Label(self, text = "MinX", padx = 3, pady = 3)
        self.label1.grid(row = 0, column = 0)
        
        self.entry1 = Tkinter.Entry(self)
        self.entry1.grid(row = 0, column = 1)

        #MaxX
        self.label2 = Tkinter.Label(self, text = "MaxX", padx = 3, pady = 3)
        self.label2.grid(row = 0, column = 2)
        
        self.entry2 = Tkinter.Entry(self)
        self.entry2.grid(row = 0, column = 3)

        #MinY
        self.label3 = Tkinter.Label(self, text = "MinY", padx = 3, pady = 3)
        self.label3.grid(row = 1, column = 0)
        
        self.entry3 = Tkinter.Entry(self)
        self.entry3.grid(row = 1, column = 1)

        #MaxY
        self.label4 = Tkinter.Label(self, text = "MaxY", padx = 3, pady = 3)
        self.label4.grid(row = 1, column = 2)
        
        self.entry4 = Tkinter.Entry(self)
        self.entry4.grid(row = 1, column = 3)

        #Z
        self.label5 = Tkinter.Label(self, text = "Z(x,y)", padx = 3, pady = 3)
        self.label5.grid(row = 2, column = 0)

        self.entry5 = Tkinter.Entry(self)
        self.entry5.grid(row = 2, column = 1)

        #Plot
        self.button1 = Tkinter.Button(self, text="Plot Function", command=self.plotData, anchor=W, padx=8)
        self.button1.grid(row = 3, column = 1)

        #Clear
        self.button2 = Tkinter.Button(self, text="Clear", command=self.clear, anchor=W, padx=8)
        self.button2.grid(row = 3, column = 3)

        #Color stuffs
        self.label6 = Tkinter.Label(self, text = "Color:", padx = 3, pady = 3)
        self.label6.grid(row = 2, column = 2)

        colorList = ["Blues", "Greens", "Oranges", "Purples", "Reds", "Greys", "pink"]

        self.var = Tkinter.StringVar()
        self.var.set(colorList[2])
        
        self.entry6 = Tkinter.OptionMenu(self, self.var, *colorList)
        self.entry6.grid(row=2,column=3)

        img = Tkinter.PhotoImage(file ="Instructions.gif")
        self.panel = Tkinter.Label(self, image = img)
        self.panel.image = img
        self.panel.grid(row = 4, column = 0, columnspan=4,rowspan=1)
        

    def clear(self):
        self.entry1.delete(0,END)
        self.entry2.delete(0,END)
        self.entry3.delete(0,END)
        self.entry4.delete(0,END)
        self.entry5.delete(0,END)

    def get_function(self):
        return self.entry5.get()

    def get_upper_x(self):
        return self.entry2.get()

    def get_lower_x(self):
        return self.entry1.get()

    def get_upper_y(self):
        return self.entry4.get()

    def get_lower_y(self):
        return self.entry3.get()

##    def getColor(self):
##        return self.entry6.get()

    def plotData(self):
        try:
            infix = self.get_function()
            infix = infix.replace(" ","")
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

            # Assign necessary variables to the self.X,Y,Z
            
            self.X = X
            self.Y = Y
            self.Z = Z
            self.hasData = True
            self.colorVal = self.var.get()

        except Exception as e:
            self.inputError()

    def inputError(self):
        print "Input Error!"
    
    def hasNewData(self):
        return self.hasData

    def consumeData(self):
        self.hasData = False

    def getData(self):
        return self.X, self.Y, self.Z, self.colorVal
