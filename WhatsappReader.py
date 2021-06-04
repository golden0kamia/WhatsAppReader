from tkinter import *
import tkinter.font as tkFont
from tkinter.filedialog import *
from tkinter.simpledialog import *

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
known = False
guyR = ""

def splitLine(text, lastData):
    if(text[0] >= '0' and text[0] <= '9' and text[2] == '.'): #Check if is a date and hour
        stop0 = text.find(" à ") #End of date
        stop1 = text.find(" - ", stop0) #End of hour
        stop2 = text.find(': ', stop1) #End of sender name
        day = text[:stop0]
        hour = text[stop0+3:stop1]
        if(stop2 == -1):
            guy = "whatsapp"
            msg = text[stop1+3:]
        else:
            guy = text[stop1+3:stop2]
            msg = text[stop2+2:]
    else:
        day = lastData[0]
        hour = lastData[1]
        guy = lastData[2]
        msg = lastData[3] + text
    #print("time: "+day+" - "+hour)
    #print("guy: "+guy)
    #print("msg: "+msg)
    return (day, hour, guy, msg)

def writeMessage(message):
    if(message[3]==""):
        return
    bubble = Frame(second_Frame, relief='groove', borderwidth=2, padx=5)
    if(message[2] == guyR):    #Write message of person 1 with hour in the right part of the screen
        bubble.configure(bg='#DCF8C6')
        if(not known):
            Label(bubble, text=message[2], bg='#DCF8C6', fg='gray', font=('Helvetica', '8')).pack(anchor='nw')
        Label(bubble, text=message[3][:-1], wraplength=300, anchor='nw', justify='right', bg='#DCF8C6').pack()
        Label(bubble, text=message[1], bg='#DCF8C6', fg='gray', font=('Helvetica', '8')).pack(anchor='ne')
        bubble.pack(pady=3, anchor='ne', padx=20)
    else:                       #Write message of people 2 with hour and name in the left part of the screen (whatsapp group is possible)
        bubble.configure(bg='#ffffff')
        Label(bubble, text=message[2], bg='#ffffff', fg='gray', font=('Helvetica', '8')).pack(anchor='nw')
        Label(bubble, text=message[3][:-1], wraplength=300, anchor='nw', justify='left', bg='#ffffff').pack()
        Label(bubble, text=message[1], bg='#ffffff', fg='gray', font=('Helvetica', '8')).pack(anchor='ne')
        bubble.pack(pady=3, anchor='nw')

def openFile():
    global guyR
    global known
    guyR = askstring("WhatsApp name", "Write your WhatsApp name or leave blank")
    print("guy name ;" + guyR + ";")
    if(not guyR == ""):
        known = True
    print(known)
    lastMssg = ["", "", "", ""]
    filePath = askopenfilename(title="Selectionner le fichier de discussion", filetypes=[('Text files','.txt')])
    fileData = open(filePath, mode='r',encoding='utf-8' )
    #while True:
    for x in range(0, 200):
        message = fileData.readline()
        #print("msg = ;" + message + ";")
        if (message == ""):
            #print("File read ended")
            break
        mssg = splitLine(message, lastMssg)

        if(mssg[2] != "" and guyR == "" and mssg[2] != "whatsapp"):
            guyR = mssg[2]       

        if(lastMssg[0] != mssg[0] and mssg[0] != ""):     #Date changed -> write in chat
            #print("--Label date --")
            Label(second_Frame, text=mssg[0], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5).pack(anchor='n')
            
        if(mssg[2] == "whatsapp"):                        #Write whatsapp info message
            #print("--Label info --")
            Label(second_Frame, text=mssg[3], wraplength=300, anchor='nw', justify='center', relief='groove', bg='#E1F3FB', padx=5, font=('Helvetica', '8')).pack(anchor='n')
        elif(((lastMssg[2] != mssg[2] and mssg[2] != "") or (lastMssg[1] != mssg[1] and mssg[1] != "") or not(lastMssg[3] in mssg[3]))
             and lastMssg[2] != "whatsapp" ):     #Guy, time or message changed -> write message
            #print("--Label mssg --")
            writeMessage(lastMssg)
        lastMssg = mssg
    writeMessage(lastMssg) #Write last message



menubar = Menu(win, tearoff=0)
menuFichier = Menu(menubar)
menuFichier.add_command(label="Ouvrir", command=openFile)
menuFichier.add_separator()
menuFichier.add_command(label="Quitter")
menubar.add_cascade(label="Fichier", menu=menuFichier)

win.config(menu=menubar)

win.mainloop()
