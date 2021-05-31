from tkinter import *
import tkinter.font as tkFont
from tkinter.filedialog import *

#hourFont = tkFont.Font(family='Helvetica', size=36, weight='bold')

win = Tk()

main_Frame = Frame(win)
main_Frame.pack(fill=BOTH, expand=1)

my_Canvas = Canvas(main_Frame)
my_Canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_Scrollbar = Scrollbar(main_Frame, command=my_Canvas.yview)
my_Scrollbar.pack(side=RIGHT, fill=Y)

my_Canvas.configure(yscrollcommand=my_Scrollbar.set)
my_Canvas.bind('<Configure>', lambda e: my_Canvas.configure(scrollregion=my_Canvas.bbox("all")))

second_Frame = Frame(my_Canvas)

my_Canvas.create_window((0, 0), window=second_Frame, anchor="nw")

filePath = ""

def splitLine(text, lastGuy):
    if(text[0] >= '0' and text[0] <= '9'):
        stop0 = text.find(" à ")
        stop1 = text.find(" - ", stop0)
        stop2 = text.find(':', stop1)
        day = text[:stop0]
        hour = text[stop0+3:stop1]
        if(stop2 == -1):
            guy = "whatsapp"
            msg = text[stop1+3:]
        else:
            guy = text[stop1+3:stop2]
            msg = text[stop2+2:]
    else:
        day = ""
        hour = ""
        guy = lastGuy
        msg = text
    #print("time: "+time)
    #print("guy: "+guy)
    #print("msg: "+msg)
    return (day, hour, guy, msg)

def openFile():
    guyL = ""
    lastGuy = ""
    lastDay = ""
    filePath = askopenfilename(title="Selectionner le fichier de discussion", filetypes=[('Text files','.txt')])
    fileData = open(filePath, mode='r',encoding='utf-8' )
    while True:
    #for x in range(0, 1000):
        bubble = Frame(second_Frame, relief='groove', borderwidth=2, padx=5)
        message = fileData.readline()
        if (message == ""):
            break
        mssg = splitLine(message, lastGuy)
        if(mssg[0] != lastDay and mssg[0] != ""):
            Label(second_Frame, text=mssg[0], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(anchor='n')
            lastDay = mssg[0]
        if(mssg[2] == "whatsapp"):
            Label(second_Frame, text=mssg[3], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(anchor='n')
            lastGuy = "whatsapp"
        elif(mssg[2] == guyL or guyL == ""):
            guyL = mssg[2]
            bubble.configure(bg='#ffffff')
            Label(bubble, text=mssg[3], wraplength=300, anchor='nw', justify='left', bg='#ffffff').pack(pady=0)
            Label(bubble, text=mssg[1], bg='#ffffff', fg='gray', font=('Helvetica', '8')).pack(anchor='nw', pady=0)
            bubble.pack(pady=3, anchor='nw')
            lastGuy = guyL
        else:
            bubble.configure(bg='#DCF8C6')
            Label(bubble, text=mssg[3], wraplength=300, anchor='nw', justify='left', bg='#DCF8C6').pack(pady=0)
            Label(bubble, text=mssg[1], bg='#DCF8C6', fg='gray', font=('Helvetica', '8')).pack(anchor='ne', pady=0)
            bubble.pack(pady=3, anchor='ne', padx=20)
            lastGuy = mssg[2]
        #bubble.pack()



menubar = Menu(win, tearoff=0)
menuFichier = Menu(menubar)
menuFichier.add_command(label="Ouvrir", command=openFile)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter")
menubar.add_cascade(label="Fichier", menu=menuFichier)

win.config(menu=menubar)

win.mainloop()
