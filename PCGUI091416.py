
# coding: utf-8

# In[2]:

false = False
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import matplotlib.pyplot as plt
import pylab as pl

UIDArray = []
Time = []
Offsettime = 0
Temp = []
        
def callback():
    file = open(askopenfilename(),'r')
    createWidgets(root, file)
    
def createWidgets(root, file):
    labelname.destroy()
    Label(root, text=file.name).place(x=100,y=0)
    location.append(file.name)
    fileo(file.name)

def fileo(filename):

    print ("Location is" , filename)

    file = open(filename,"r")
    readflag = False
    newdata = False
    sting = file.readline()
    Offsettime = 0
    while len(sting) != 0:
        string= sting.split(" ")

        if(readflag == True):
            readflag = False

            if(string[17] == "OK\n"):
                #calculate temp 
                tempvalue =string[11]+string[12]
                i = int(tempvalue, 16)


                #calcualte time
                timearray= string[1].split(":")
                temptime = float(timearray[0])*3600+float(timearray[1])*60+float(timearray[2]);

                index = UIDArray.index(UID)
                if(Offsettime == 0):
                    Offsettime = temptime

                Time[index].append(temptime- Offsettime)
                i = i *.169 - 92.7-5.4
                Temp[index].append(i)


        if(string[7] == "12"):
            readflag = True
            UID = ''
            for i in range(0,8):
                UID+= string[i+13]
            if(UID not in UIDArray):
                size = len(UIDArray)

                UIDArray.append(UID)

                Time.append([])
                Temp.append([])
            
        sting = file.readline()
    printUID()
    
def printUID():
    print(UIDArray)
    for x in (UIDArray):
        listNodes.insert(END, str(x))

    listNodes.bind('<<ListboxSelect>>', onselect)
    

def onselect(event): 
    w = event.widget
    index = int(w.curselection()[0])
    print(index)
    value = w.get(index)
    n=0
    for i in indexs:
        if index == i:
            n = 1
    if n ==0:
        indexs.append(index)
        listSelection.insert(END, "Node ID: " + str(UIDArray[index]))
        param(index)
    
def param(index):
    e2.delete(0, END)
    if (float(e3.get())<Time[index][-1]):
        e3.delete(0, END)
        e3.insert(0, Time[index][-1])   
    e2.insert(0, 0)
    if Temp[index][0] < float(e4.get()) or float(e4.get())==0:
        e4.delete(0, END)
        e4.insert(0, Temp[index][0]-10)       
    if Temp[index][-1] > float(e5.get()):
        e5.delete(0, END)
        e5.insert(0, Temp[index][-1]+10)

def plotall():
    graph = []
#     nameset = []
    for i in indexs:
        gph = pl.plot(Time[i],Temp[i], Label="UID: %s"%UIDArray[i])
        pl.legend()
    pl.xlabel('Time [s]')
    pl.ylabel('Temperature [°C]')
    pl.title('Temp vs. Time')
    pl.axis([float(e2.get()),float(e3.get()),float(e4.get()), float(e5.get())])

    pl.show()

def reset():
    while len(indexs) != 0:
        indexs.pop(0)
    listSelection.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e2.insert(0, 0)
    e3.insert(0, 0)
    e4.insert(0, 0)
    e5.insert(0, 0)
    
def export():
    wfile = open("D:/Desktop/Python GUI Log/log_(%s).txt"%os.path.basename(location[0]), 'w')
    for i in indexs:
        wfile.write("%-50s" %UIDArray[i])
    wfile.write("\n")
    wfile.write("\n")
    k = -1
    j = 0

    while j < len(indexs):
        j = 0
        for i in indexs:
            if k == -1:
                wfile.write("%-25s" %"Time(s)")
                wfile.write("%-25s" %"Temperature(C)")
            if len(Time[i])>k and k != -1:
                wfile.write("%-25s" %str(Time[i][k]))
                wfile.write("%-25s" %str(Temp[i][k]))
            elif len(Time[i])<=k and k != -1:
                wfile.write("%-25s" %"")
                wfile.write("%-25s" %"")
                j = j + 1
        wfile.write("\n")
        k = k + 1        
            
    wfile.close()

# main
root = Tk()
root.pack_propagate(0)
root.title("PC GUI")
root.geometry("550x200")

timedft=0
# Menu Bar-------------------------------------------------------------------------------------------------        
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=callback)

menubar.add_cascade(label="Menu", menu=filemenu)
root.config(menu=menubar)
# Menu Bar-------------------------------------------------------------------------------------------------        

# Labels----------------------------------------------------------------------------------------------------       
Label(root, text="File Name: ").place(x=0, y=0)
labelname = Label(root, text="Please Choose the Log File")
labelname.place(x=100,y=0)

lbl1 = Label(root, text="UID List:", fg='black', font=("Helvetica", 16, "bold"))
lbl1.place(x=0, y=30)
lbl1 = Label(root, text="Details:", fg='black', font=("Helvetica", 16, "bold"))
lbl1.place(x=200, y=30)

###############

scrollbar = Scrollbar(root, orient="vertical")
lb12 = listNodes = Listbox(root, width=18, height=6, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
scrollbar.config(command=listNodes.yview)
lb12.place(x=5, y =55)

##############

xstart = Label(root, text="Time Start: ")
xstart.place(x= 200, y = 120)
e2 = Entry(root, width=8)
e2.place(x= 265, y = 120)
e2.insert(END, 0)
xstart = Label(root, text="(s)")
xstart.place(x= 315, y = 120)

xstart = Label(root, text="Time End: ")
xstart.place(x= 200, y = 145)
e3 = Entry(root, width=8)
e3.place(x= 265, y = 145)
e3.insert(END, 0)
xstart = Label(root, text="(s)")
xstart.place(x= 315, y = 145)

xstart = Label(root, text="Temp Start: ")
xstart.place(x= 350, y = 120)
e4 = Entry(root, width=8)
e4.place(x= 455, y = 120)
e4.insert(END, 0)
xstart = Label(root, text="°C")
xstart.place(x= 505, y = 120)

xstart = Label(root, text="Temp End: ")
xstart.place(x= 350, y = 145)
e5 = Entry(root, width=8)
e5.place(x= 455, y = 145)
e5.insert(END, 0)
xstart = Label(root, text="°C")
xstart.place(x= 505, y = 145)

listSelection = Listbox(root, width=36, height=3, font=("Helvetica", 12))
listSelection.place(x=200, y=55)

indexs=[]
location = []



b1 = Button(root, text='Graph', command=plotall)
b1.place(x = 200, y = 170)
b2 = Button(root, text='Reset', command=reset)
b2.place(x = 260, y = 170)
b3 = Button(root, text='Export .txt', command=export)
b3.place(x = 320, y = 170)
# Labels----------------------------------------------------------------------------------------------------

root.mainloop()


# In[ ]:




# In[ ]:



