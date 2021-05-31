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

def splitLine(text, lastGuy, lastMsg):
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
        msg = lastMsg + text
    #print("time: "+time)
    #print("guy: "+guy)
    #print("msg: "+msg)
    return (day, hour, guy, msg)

def openFile():
    guyL = ""
    lastDay = ""
    lastHour = ""
    lastGuy = ""
    lastMsg = ""
    filePath = askopenfilename(title="Selectionner le fichier de discussion", filetypes=[('Text files','.txt')])
    fileData = open(filePath, mode='r',encoding='utf-8' )
    while True:
    #for x in range(0, 1000):
        message = fileData.readline()
        if (message == ""):
            break
        mssg = splitLine(message, lastGuy, lastMsg)
        
        if(mssg[2] == "whatsapp"):  #Write First info message
            Label(second_Frame, text=mssg[0], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(anchor='n')
            lastDay = mssg[0]
            Label(second_Frame, text=mssg[3], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(anchor='n')
            lastGuy = "firstGuy"
        elif(lastGuy == "firstGuy"):
            lastHour = mssg[1]
            lastGuy = mssg[2]
            lastMsg = mssg[3]
        elif(mssg[2] != lastGuy):
            bubble = Frame(second_Frame, relief='groove', borderwidth=2, padx=5)
            if(mssg[2] == guyL or guyL == ""):    #Write message of person 1 with hour
                guyL = mssg[2]
                bubble.configure(bg='#ffffff')
                Label(bubble, text=lastMsg, wraplength=300, anchor='nw', justify='left', bg='#ffffff').pack()
                Label(bubble, text=lastHour, bg='#ffffff', fg='gray', font=('Helvetica', '8')).pack(anchor='nw')
                bubble.pack(pady=3, anchor='nw')
                lastGuy = guyL
            else:                                   #Write message of person 2 with hour
                bubble.configure(bg='#DCF8C6')
                Label(bubble, text=lastMsg, wraplength=300, anchor='nw', justify='left', bg='#DCF8C6').pack()
                Label(bubble, text=lastHour, bg='#DCF8C6', fg='gray', font=('Helvetica', '8')).pack(anchor='ne')
                bubble.pack(pady=3, anchor='ne', padx=20)
                lastGuy = mssg[2]
            if(mssg[0] != lastDay and mssg[0] != ""):   #Write date in chat
                Label(second_Frame, text=mssg[0], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(anchor='n')
                lastDay = mssg[0]
            lastDay = mssg[0]
            lastHour = mssg[1]
            lastMsg = mssg[3]
        else:
            lastMsg = mssg[3]
        #lastDay = mssg[0]
        #lastHour = mssg[1]
        #lastGuy = mssg[2]
        #lastMsg = mssg[3]



menubar = Menu(win, tearoff=0)
menuFichier = Menu(menubar)
menuFichier.add_command(label="Ouvrir", command=openFile)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter")
menubar.add_cascade(label="Fichier", menu=menuFichier)

win.config(menu=menubar)

win.mainloop()
