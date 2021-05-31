from tkinter import *
from tkinter.filedialog import *

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
        stop1 = text.find(" - ")
        stop2 = text.find(':', stop1)
        time = text[:stop1]
        if(stop2 == -1):
            guy = "whatsapp"
            msg = text[stop1+3:]
        else:
            guy = text[stop1+3:stop2]
            msg = text[stop2+2:]
    else:
        time = ""
        guy = lastGuy
        msg = text
    #print("time: "+time)
    #print("guy: "+guy)
    #print("msg: "+msg)
    return (time, guy, msg)

def openFile():
    guyL = ""
    lastGuy = ""
    filePath = askopenfilename(title="Selectionner le fichier de discussion", filetypes=[('Text files','.txt')])
    fileData = open(filePath, mode='r',encoding='utf-8' )
    while(message != ""):
    #for x in range(0, 1000):
        message = fileData.readline()
        mssg = splitLine(message, lastGuy)
        if(mssg[1] == "whatsapp"):
            Label(second_Frame, text=mssg[2], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(pady=3, anchor='n')
            lastGuy = "whatsapp"
        elif(mssg[1] == guyL or guyL == ""):
            guyL = mssg[1]
            Label(second_Frame, text=mssg[2], wraplength=300, anchor='nw', justify='left', relief='groove', bg='#ffffff', padx=5).pack(pady=3, anchor='nw')
            lastGuy = guyL
        else:
            Label(second_Frame, text=mssg[2], wraplength=300, anchor='nw', justify='left', relief='groove', bg='#DCF8C6', padx=5).pack(pady=3, anchor='ne', padx=20)
            lastGuy = mssg[1]



menubar = Menu(win, tearoff=0)
menuFichier = Menu(menubar)
menuFichier.add_command(label="Ouvrir", command=openFile)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter")
menubar.add_cascade(label="Fichier", menu=menuFichier)

win.config(menu=menubar)

win.mainloop()
