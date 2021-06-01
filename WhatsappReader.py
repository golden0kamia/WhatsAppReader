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
        stop2 = text.find(': ', stop1)
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
    print("time: "+day+" - "+hour)
    print("guy: "+guy)
    print("msg: "+msg)
    return (day, hour, guy, msg)

def writeMessage(message, guyL):
    if(message[3]==""):
        return
    bubble = Frame(second_Frame, relief='groove', borderwidth=2, padx=5)
    if(message[2] == guyL):    #Write message of person 1 with hour
        bubble.configure(bg='#ffffff')
        Label(bubble, text=message[2], bg='#ffffff', fg='gray', font=('Helvetica', '8')).pack(anchor='nw')
        Label(bubble, text=message[3], wraplength=300, anchor='nw', justify='left', bg='#ffffff').pack()
        Label(bubble, text=message[1], bg='#ffffff', fg='gray', font=('Helvetica', '8')).pack(anchor='nw')
        bubble.pack(pady=3, anchor='nw')
    else:                       #Write message of person 2 with hour
        bubble.configure(bg='#DCF8C6')
        Label(bubble, text=message[2], bg='#DCF8C6', fg='gray', font=('Helvetica', '8')).pack(anchor='ne')
        Label(bubble, text=message[3], wraplength=300, anchor='nw', justify='left', bg='#DCF8C6').pack()
        Label(bubble, text=message[1], bg='#DCF8C6', fg='gray', font=('Helvetica', '8')).pack(anchor='ne')
        bubble.pack(pady=3, anchor='ne', padx=20)

def openFile():
    guyL = ""
    lastMssg = ["", "", "", ""]
    filePath = askopenfilename(title="Selectionner le fichier de discussion", filetypes=[('Text files','.txt')])
    fileData = open(filePath, mode='r',encoding='utf-8' )
    #while True:
    for x in range(0, 100):
        message = fileData.readline()
        if (message == ""):
            break
        mssg = splitLine(message, lastMssg[2], lastMssg[3])

        if(mssg[2] != "" and guyL == "" and mssg[2] != "whatsapp"):
            guyL = mssg[2]       

        if(mssg[2] == "whatsapp"):                          #Write whatsapp info message
            Label(second_Frame, text=mssg[3], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5, font=('Helvetica', '8')).pack(anchor='n')
            lastMssg[2] = mssg[2]
        elif(lastMssg[0] != mssg[0] and mssg[0] != ""):     #Date changed -> write in chat
            Label(second_Frame, text=mssg[0], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(anchor='n')
        if(lastMssg[2] != mssg[2] and mssg[2] != "" and lastMssg[2] != "whatsapp"):       #Guy changed -> write message
            writeMessage(lastMssg, guyL)
        elif(lastMssg[1] != mssg[1] and mssg[1] != ""):     #Time changes -> write message
            writeMessage(lastMssg, guyL)
        lastMssg = mssg



menubar = Menu(win, tearoff=0)
menuFichier = Menu(menubar)
menuFichier.add_command(label="Ouvrir", command=openFile)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter")
menubar.add_cascade(label="Fichier", menu=menuFichier)

win.config(menu=menubar)

win.mainloop()
