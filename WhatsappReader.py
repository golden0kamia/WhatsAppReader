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

def splitLine(text):
    if(text[0] >= '0' and text[0] <= '9'):
        stop1 = text.find(" - ")
        stop2 = text.find(':', stop1)
        time = text[:stop1]
        guy = text[stop1+3:stop2]
        msg = text[stop2+2:]
        #print("time: "+time)
        #print("guy: "+guy)
        #print("msg: "+msg)
    else:
        time = ""
        guy = ""
        msg = text
    return (time, guy, msg)

def openFile():
    guyG = ""
    filePath = askopenfilename(title="Selectionner le fichier de discussion", filetypes=[('Text files','.txt')])
    fileData = open(filePath, mode='r',encoding='utf-8' )
    message = fileData.readline()
    message = fileData.readline()
    while(message != ""):
        mssg = splitLine(message)
        if(guyG == ""):
            guyG = mssg[1]
        elif(mssg[1] == guyG):
            Label(second_Frame, text=mssg[2], wraplength=300, anchor='nw', justify='left', relief='groove', bg='#b4ff63', padx=5).pack(pady=3, anchor='nw')
        else:
            Label(second_Frame, text=mssg[2], wraplength=300, anchor='nw', justify='left', relief='groove', bg='#40ff93', padx=5).pack(pady=3, anchor='ne', padx=20)
        message = fileData.readline()



menubar = Menu(win, tearoff=0)
menuFichier = Menu(menubar)
menuFichier.add_command(label="Ouvrir", command=openFile)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter")
menubar.add_cascade(label="Fichier", menu=menuFichier)

win.config(menu=menubar)

win.mainloop()
