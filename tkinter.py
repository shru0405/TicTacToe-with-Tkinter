import tkinter as tk
from tkinter import Frame as fr


class mainapp(tk.Tk):
    def __init__(self, *args):
        tk.Tk.__init__(self, *args)
        self.title('Tic Tac Toe V1.0')
        self.update()

#After forcing the instance to update,determine the width of the screen and window borders.
        
        self.width = int(self.winfo_screenwidth()) * 0.4
        self.screenwidth = int(self.winfo_screenwidth())
        self.x_border = int(self.winfo_rootx() - self.winfo_x())
        self.x_start = self.screenwidth / 2 - (self.width / 2 + self.x_border)

#Determine height using same methods.
        self.height = self.width * 1.08
        self.screenheight = int(self.winfo_screenheight())
        self.y_border = int(self.winfo_rooty() - self.winfo_y())
        self.y_start = self.screenheight / 2 - (self.height / 2 + self.y_border)

#Use width/height to open window to relative size (resolution independent) and centered.

        self.geometry('%dx%d+%d+%d' % (self.width, self.height, int(self.x_start), int(self.y_start)))
        self.resizable('false', 'false')

#Will determine if X's turn or O's turn.
        mainapp.clickcount = 0

#One frame for X's and O's and one for restart button.
        mainapp.F1 = fr(bg='#121212')
        self.F2 = fr(bg='#121212')
        mainapp.F1.grid(row=0, column=0, sticky='nsew')
        self.F2.grid(row=1, column=0, sticky='nsew')
        self.F2.grid_columnconfigure(0, weight=1)

        restart = tk.Button(self.F2, text='RESTART',
                            relief='flat',
                            borderwidth=2,
                            font=('verdana', 12, 'bold'),
                            fg='white',
                            bg='#333333',
                            command=self.restart)
        restart.grid(row=1, column=0, sticky='ew')

#Row:Column coordinates of the diagonal places.
        mainapp.diagonal1 = {1: 0, 2: 1, 3: 2}
        mainapp.diagonal2 = {3: 0, 2: 1, 1: 2}
        
#Need to handle X's and O's separately.
#Creating these lists here so that we only need to do it once and are free to access them from each X or O.
# Will append relevant values each time an X or O is activated.
        mainapp.rowsX = []
        mainapp.columnsX = []
        mainapp.rowsO = []
        mainapp.columnsO = []
        
#Win1 is used for one diagonal direction, Win2 for the other.
        mainapp.XWin1 = []
        mainapp.XWin2 = []
        mainapp.OWin1 = []
        mainapp.OWin2 = []

#Used to explictly state the rows/columns to use - allows a condensed structure for loop structure,i.e. 3 rows * 3 columns + 9 buttons vs 3 rows * 3 columns * 9 buttons.
        
        self.rows_cols = []
        
 #Keeping this outside of the buttoncreation function so that the grid is only created instantiation, of the main class; 
 #it doesn't have to be reloaded when the restart function runs.
 #Avoiding row 0 by convention, in case a title bar is added later.
        
        for row in range(1, 4):
            for column in range(3):
                rc = '{0}:{1}'.format(row, column)
                self.rows_cols.append(rc)
        self.buttoncreation()

    def buttoncreation(self):
        for item in self.rows_cols:
            button = item
            self.button = XO(mainapp.F1)
            self.button.grid(row=item[0], column=item[2])

    def restart(self):
#Resets clickcount while maintaining the turn cycle.
       
        mainapp.clickcount = 0 + (mainapp.clickcount % 2)
        
#Removes all of the buttons at once, then recreates their parent frame.
        mainapp.F1.destroy()
        mainapp.F1 = fr(bg='#121212')
        mainapp.F1.grid(row=0, column=0, sticky='nsew')
        
#Clears the lists to prevent inappropriate win calculation.
        mainapp.rowsX.clear()
        mainapp.columnsX.clear()
        mainapp.rowsO.clear()
        mainapp.columnsO.clear()
        mainapp.XWin1.clear()
        mainapp.XWin2.clear()
        mainapp.OWin1.clear()
        mainapp.OWin2.clear()

        self.buttoncreation()


class XO(tk.Button):
    def __init__(self, *args):
        tk.Button.__init__(self, *args)

#Each X or O is a custom gif.When clicked, the buttons disable and change to an 'active' colour.

        PhotoImage = tk.PhotoImage
        self.pic = PhotoImage(file='TicTacToeBefore.gif')
        self.picx = PhotoImage(file='XActive.gif')
        self.winx = PhotoImage(file='XWin.gif')
        self.pico = PhotoImage(file='OActive.gif')
        self.wino = PhotoImage(file='OWin.gif')

        self.config(self, bg='#121212',
                    borderwidth=1,
                    relief='flat',
                    image=self.pic,
                    command=self.engage)
        self.image = self.pic

    def engage(self):

#X activation occurs during even turns.
        if mainapp.clickcount % 2 != 0:

            self.config(image=self.picx, state='disabled')
            self.image = self.picx
            
#Paramaterisation of the relevant lists and image.
#Allows analysis function to only be written once.

            rowsz = mainapp.rowsX
            columnsz = mainapp.columnsX
            ZWin1 = mainapp.XWin1
            ZWin2 = mainapp.XWin2
            winz = self.winx
            self.analysis(rowsz, columnsz, ZWin1, ZWin2, winz)

 #Same as above but for O's.
 
        elif mainapp.clickcount % 2 == 0:
            self.config(image=self.pico, state='disabled')
            self.image = self.pico
            rowsz = mainapp.rowsO
            columnsz = mainapp.columnsO
            ZWin1 = mainapp.OWin1
            ZWin2 = mainapp.OWin2
            winz = self.wino
            self.analysis(rowsz, columnsz, ZWin1, ZWin2, winz)

    def analysis(self, rowsz, columnsz, zWin1, zWin2, winz):

  #Need to retrieve the position information of each X or O prior to analysing it.
  
        self.positioning = self.grid_info()
        self.row = self.positioning.get('row')
        self.column = self.positioning.get('column')

        rowsz.append(self.row)
        columnsz.append(self.column)

 #Treating each diagonal separately.
 #Appending row and column data because it is needed in order to change the image when a diagonal win occurs.
        if self.row in mainapp.diagonal1.keys() and self.column == mainapp.diagonal1.get(self.row):
            zWin1.append(self.row)
            zWin1.append(self.column)
        if self.row in mainapp.diagonal2.keys() and self.column == mainapp.diagonal2.get(self.row):
            zWin2.append(self.row)
            zWin2.append(self.column)

#At least 3 X's or O's.
#Treating rows and columns separately.
#Changes the image of winning X's or O's.

        if len(rowsz) >= 3:
            for item in rowsz:
                if rowsz.count(item) == 3:
                    for slave in mainapp.F1.grid_slaves(row=item):
                        slave.config(image=winz)
                    zwin = True
            for item in columnsz:
                if columnsz.count(item) == 3:
                    for slave in mainapp.F1.grid_slaves(column=item):
                        slave.config(image=winz)
                    zwin = True

        try:
            if zwin == True:
   #Disables all buttons that aren'tactive,i.e. aren't X's or O's.
                self.blocking()
        except:
#3 rows + 3 columns.
#Odds are rows - both used to change image on winning.
#Analysing each diagonal separately.

            if len(zWin1) == 6:
                for i in range(6):
                    if i % 2 == 0:
                        for slave in mainapp.F1.grid_slaves(row=zWin1[i], column=zWin1[int(i) + 1]):
                            slave.config(image=winz)
                self.blocking()

            elif len(zWin2) == 6:
                for i in range(6):
                    if i % 2 == 0:
                        for slave in mainapp.F1.grid_slaves(row=zWin2[i], column=zWin2[int(i) + 1]):
                            slave.config(image=winz)
            self.blocking()

        #         Changes turn after each click that occurs before a win.
        mainapp.clickcount += 1

    def blocking(self):
    
#Maintains turn changing and prevents play from continuing after a win.
#Does this by disabling unclicked buttons.

        mainapp.clickcount += 1
        for each in mainapp.F1.grid_slaves():
            x = each.config()
            y = str(x.get('state'))
            if 'disabled' not in y:
                each.config(state='disabled')


# Instantiating and calling the app.
tictactoe = mainapp()
tictactoe.mainloop()
