import os
from tkinter import *
from tkinter import filedialog
import pyglet
import threading



thisfolder = os.path.dirname(os.path.realpath(__file__)) + "\\"
clickcounter = 0
selected_dir = ""
qc_selected_dir = ""
qc_selected_dir = ""
parameters_replacement_list = []
parameters_search_for_list = []
qc_parameters_replacement_list = []
qc_parameters_search_for_list = []
fileslist = []
lastdirectory = ""
qc_lastdirectory = ""
includespaces = False
screenw = 0
screenh = 0
search_sub_directories = False
replace_entire_line = False
epicvalue = -1
edit_options_enabled = []

#Simple Toggle
def SubFolderSwitch():
    global search_sub_directories
    if search_sub_directories == False:
        search_sub_directories = True
        subfolderbutton.config(text="Search/Edit Files in \nSubfolders: ON")
        edit_options_enabled.append("Edit in Subfolders")
    else:
        search_sub_directories = False
        subfolderbutton.config(text="Search/Edit Files in \nSubfolders: OFF")
        edit_options_enabled.remove("Edit in Subfolders")

#Simple Toggle
def ReplaceLineSwitch():
    global replace_entire_line
    if replace_entire_line == False:
        replace_entire_line = True
        linebutton.config(text="Replace Entire Line: ON")
        edit_options_enabled.append("Replace Entire Line")
    else:
        replace_entire_line = False
        linebutton.config(text="Replace Entire Line: OFF")
        edit_options_enabled.remove("Replace Entire Line")


def PutFilesIntoList(givenpath):
    global fileslist
    for root, dirs, files in os.walk(givenpath):
        for file in files:
            fileslist.append(os.path.join(root, file))

#Startup Stuff
def Startup():
    RefreshParameterFileToList()
    pyglet.font.add_directory(thisfolder)
    root.mainloop()


# As a safety, make sure you confirm any action!
def ReplaceConfirm():
    global confirmtimer
    if len(edit_options_enabled) == 0:
        confirmtimer = threading.Timer(2.3, ResetConfirm)
        btn2.config(text=f"No middle options enabled. Confirm or wait 2 secs.",font=("TF2 Build", 16),command=ReplaceConfirmMiddle)
    else:
        confirmtimer = threading.Timer(3.2, ResetConfirm)
        btn2.config(text=f"You have options enabled.\n\n {edit_options_enabled} \n\n Confirm or wait 3 secs.",font=("TF2 Build", 16),command=ReplaceConfirmMiddle)
    confirmtimer.start()

def ResetConfirm():
    global confirmtimer
    confirmtimer.cancel()
    border_color3.pack(anchor="nw", padx=10,pady=20)
    btn2.config(text="Edit VMTs!",font=("TF2 Build", 20), command=ReplaceConfirm,bg="#2a2725", relief="flat",fg="#38F3AB", borderwidth=0,highlightthickness=0)

def ReplaceConfirmMiddle():
    global confirmtimer
    confirmtimer.cancel()
    confirmtimer = threading.Timer(3.2, ResetConfirm)
    confirmtimer.start()
    btn2.config(text=f"Super insanely ultra for suresies rn? \n\n Confirm or wait 3 secs.",font=("TF2 Build", 16),command=ReplaceVmtText)

# QC Confirms
def qcReplaceConfirm():
    global qcconfirmtimer
    border_color6.place(x=600, y=150)
    if len(edit_options_enabled) == 0:
        qcconfirmtimer = threading.Timer(2.3, qcResetConfirm)
        qcbtn6.config(text=f"No middle options\n enabled. Confirm or wait 2 secs.",font=("TF2 Build", 16),command=qcReplaceConfirmMiddle)
    else:
        qcconfirmtimer = threading.Timer(3.2, qcResetConfirm)
        qcbtn6.config(text=f"You have options enabled.\n\n {edit_options_enabled} \n\n Confirm or wait 3 secs.",font=("TF2 Build", 16),command=qcReplaceConfirmMiddle)
    qcconfirmtimer.start()    

def qcReplaceConfirmMiddle():
    global qcconfirmtimer
    qcconfirmtimer.cancel()
    qcconfirmtimer = threading.Timer(3.2, qcResetConfirm)
    qcconfirmtimer.start()
    qcbtn6.config(text=f"Super insanely ultra for suresies rn? \n\n Confirm or wait 3 secs.",font=("TF2 Build", 16),command=ReplaceQCText)

def qcResetConfirm():
    global qcconfirmtimer
    qcconfirmtimer.cancel()
    qcbtn6.config(text="Edit .qcs!",font=("TF2 Build", 20),bg="#2a2725", relief="flat",fg="#AA0000",borderwidth=0,highlightthickness=0,command=qcReplaceConfirm)
    border_color6.place(x=824, y=150)

#Parameters
def RefreshParameterFileToList():
    global qc_parameters_replacement_list
    global qc_parameters_search_for_list
    global parameters_replacement_list
    global parameters_search_for_list

    parameters_replacement_list.clear()
    parametersfile = open(thisfolder + "ParameterReplacement.txt", mode='r')
    for line in parametersfile.read().splitlines():
        parameters_replacement_list.append(line)
    parametersfile.close()

    parameters_search_for_list.clear()
    parametersearchfile = open(thisfolder + "ParameterSearch.txt", mode='r')
    for line in parametersearchfile.read().splitlines():
        parameters_search_for_list.append(line)
    parametersearchfile.close()

    qc_parameters_replacement_list.clear()
    qcparametersfile = open(thisfolder + "QcParameterReplacement.txt", mode='r')
    for line in qcparametersfile.read().splitlines():
        qc_parameters_replacement_list.append(line)
    qcparametersfile.close()

    qc_parameters_search_for_list.clear()
    qcparametersearchfile = open(thisfolder + "QcParameterSearch.txt", mode='r')
    for line in qcparametersearchfile.read().splitlines():
        qc_parameters_search_for_list.append(line)
    qcparametersearchfile.close()

#Directory Setting
def SetDirectory():
    global selected_dir
    global fileslist
    global lastdirectory
    global clickcounter
    dummydir = os.getcwd()
    try:
        selected_dir = filedialog.askdirectory(parent=root, initialdir=dummydir, title='Please select your directory')
        if len(selected_dir) > 0 and selected_dir != lastdirectory:
            lastdirectory = selected_dir
            directorydisplay.config(text=selected_dir, font="Helvetica 10 bold", fg="green")
    except:
        print("Idk how the hell it broke but it did")
        selected_dir = lastdirectory
def qc_SetDirectory():
    global qc_selected_dir
    global fileslist
    global qc_lastdirectory
    global clickcounter
    dummydir = os.getcwd()
    try:
        qc_selected_dir = filedialog.askdirectory(parent=root, initialdir=dummydir, title='Please select your directory')
        if len(qc_selected_dir) > 0 and qc_selected_dir != qc_lastdirectory:
            qc_lastdirectory = qc_selected_dir
            qc_directorydisplay.config(text=qc_selected_dir, font="Helvetica 10 bold", fg="green")
    except:
        print("Idk how the hell it broke but it did")
        qc_selected_dir = qc_lastdirectory

#Replacements Screens
def qcCreateProtectedFilesScreen():
    global thisfolder
    global fileslist
    global parameters_replacement_list
    global parameters_search_for_list
    global qc_parameters_search_for_list
    global qc_parameters_replacement_list
    def on_closing():
        with open(thisfolder + "QcParameterSearch.txt", mode='w') as filesearch:
            filesearch.write(everything_listbox.get(1.0, END))
            filesearch.close()
        with open(thisfolder + "QcParameterReplacement.txt", mode='w') as filereplace:
            filereplace.write(replace_listbox.get(1.0, END))
        protectionwindow.destroy()
    # Create a new window
    protectionwindow = Toplevel(root)
    protectionwindow.title("Edit Searches, and Replacements. Saves on close.")
    protectionwindow.protocol("WM_DELETE_WINDOW", on_closing)

    # Disable interaction with the root window
    protectionwindow.grab_set()
    # Create listboxes for everythinglist and protectedfiles
    
    everything_listbox = Text(protectionwindow)
    replace_listbox = Text(protectionwindow)

    # Layout using grid geometry manager
    everything_listbox.grid(row=0, column=0, padx=1, pady=1)
    replace_listbox.grid(row=0,column=1,padx=1,pady=1)

    with open(thisfolder + "QcParameterSearch.txt", mode='r') as filesearch:
        content = filesearch.read()
        everything_listbox.insert(END,content)
    with open(thisfolder + "QcParameterReplacement.txt", mode='r') as filereplace:
        content = filereplace.read()
        replace_listbox.insert(END,content)
def CreateProtectedFilesScreen():
    global thisfolder
    global fileslist
    global parameters_replacement_list
    global parameters_search_for_list
    global qc_parameters_search_for_list
    global qc_parameters_replacement_list
    def on_closing():
        open(thisfolder + "ParameterSearch.txt", mode='w').close()
        with open(thisfolder + "ParameterSearch.txt", mode='w') as filesearch:
            searchcontent = everything_listbox.get(1.0, END).rstrip('\n')
            filesearch.write(searchcontent)
        open(thisfolder + "ParameterReplacement.txt", mode='w').close()
        with open(thisfolder + "ParameterReplacement.txt", mode='w') as filereplace:
            replacecontent = replace_listbox.get(1.0, END).rstrip('\n')
            filereplace.write(replacecontent)
        RefreshParameterFileToList()
        protectionwindow.destroy()
    # Create a new window
    protectionwindow = Toplevel(root)
    protectionwindow.title("Edit Searches, and Replacements. Saves on close.")
    protectionwindow.protocol("WM_DELETE_WINDOW", on_closing)

    # Disable interaction with the root window
    protectionwindow.grab_set()
    # Create listboxes for everythinglist and protectedfiles
    
    everything_listbox = Text(protectionwindow)
    replace_listbox = Text(protectionwindow)

    # Layout using grid geometry manager
    everything_listbox.grid(row=0, column=0, padx=1, pady=1)
    replace_listbox.grid(row=0,column=1,padx=1,pady=1)

    with open(thisfolder + "ParameterSearch.txt", mode='r') as filesearch:
        content = filesearch.read()
        everything_listbox.insert(END,content)
    with open(thisfolder + "ParameterReplacement.txt", mode='r') as filereplace:
        content = filereplace.read()
        replace_listbox.insert(END,content)

# MAIN WINDOW #########################################################################################
root = Tk()
def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

root.overrideredirect(True) # turns off title bar, geometry
root.geometry('1000x400+500+300') # set new geometry
root.config(bg="#1c1a19")
# Make a frame for the title bar
title_bar = Frame(root, bg='#0f0d0d', relief='raised')

#Put a close button on the title bar
close_button = Button(title_bar, text='X', command=root.destroy,fg="red3",background="#0f0d0d", font=("TF2 Build", 20),highlightbackground="black",highlightcolor="pink")
vmt_section = Label(title_bar, text="VMTS", fg="white", font=("TF2 Build", 16),bg="#0f0d0d")
compile_decompile = Label(title_bar, text="OPTIONS", fg="white", font=("TF2 Build", 16),bg="#0f0d0d")
CQ_section = Label(title_bar, text="QCs", fg="white", font=("TF2 Build", 16),bg="#0f0d0d")

#A canvas for the main area of the window
window = Canvas(root, height=1000,width=1000, bg="#1c1a19")

#Packin the widgets
title_bar.pack(fill="x", side="top")
close_button.pack(side="right")
CQ_section.pack(side="right",anchor="se")
vmt_section.pack(side=LEFT, anchor=S)
compile_decompile.pack(side=BOTTOM, anchor=S)
window.pack(expand=1, fill="both")
window.config(borderwidth=0,highlightthickness=0)

# bind title bar motion to the move window function
title_bar.bind('<B1-Motion>', move_window)

border_color1 = Label(window, background="#FFD700",borderwidth=1,justify="center")
border_color2 = Label(window, background="#8650AC",borderwidth=1,justify="center")
border_color3 = Label(window, background="#38F3AB",borderwidth=1,justify="center")
border_color4 = Label(window, background="#FFD700",borderwidth=1,justify="center")
border_color5 = Label(window, background="#8650AC",borderwidth=1,justify="center")
border_color6 = Label(window, background="#AA0000",borderwidth=1,justify="center")
border_color7 = Label(window, background="#bf118b",borderwidth=1,justify="center")
border_color8 = Label(window, background="#5474ab",borderwidth=1,justify="center")

# Directory things
directorydisplay = Label(window, bg="#1c1a19")
qc_directorydisplay = Label(window, bg="#1c1a19")

#Buttons for everything
#VMTS
btn1 = Button(border_color1, text="Select Directory", command=SetDirectory, font=("TF2 Build", 20),fg="#FFD700",bg="#2a2725", relief="flat",borderwidth=0,highlightthickness=0)
btn2 = Button(border_color3, text="Edit VMTs!",font=("TF2 Build", 20), command=ReplaceConfirm,bg="#2a2725", relief="flat",fg="#38F3AB", borderwidth=0,highlightthickness=0)
btn6 = Button(border_color2, text="Replacements", font=("TF2 Build", 20),bg="#2a2725", relief="flat",fg="#8650AC",borderwidth=0,highlightthickness=0,command=CreateProtectedFilesScreen)

#QCs
qcbtn1 = Button(border_color4, text="Select qc Directory", command=qc_SetDirectory, font=("TF2 Build", 20),fg="#FFD700",bg="#2a2725", relief="flat",borderwidth=0,highlightthickness=0)
qcbtn2 = Button(border_color5, text=".qc Replacements",font=("TF2 Build", 20), command=qcCreateProtectedFilesScreen,bg="#2a2725", relief="flat",fg="#8650AC", borderwidth=0,highlightthickness=0)
qcbtn6 = Button(border_color6, text="Edit .qcs!", font=("TF2 Build", 20),bg="#2a2725", relief="flat",fg="#AA0000",borderwidth=0,highlightthickness=0,command=qcReplaceConfirm)

#Subfolder Button
subfolderbutton = Button(border_color7, text="Search/Edit Files in \nSubfolders: OFF", font=("TF2 Build", 16),bg="#2a2725", relief="flat",fg="#bf118b",borderwidth=0,highlightthickness=0,command=SubFolderSwitch)

#Replace Line Button
linebutton = Button(border_color8, text="Replace Entire Line: OFF", font=("TF2 Build", 16),bg="#2a2725", relief="flat",fg="#5474ab",borderwidth=0,highlightthickness=0,command=ReplaceLineSwitch)


border_color1.pack(anchor="nw",padx=10)
directorydisplay.pack(anchor="nw", padx=10)
border_color2.pack(anchor="nw", padx=10)
border_color3.pack(anchor="nw", padx=10,pady=20)
border_color4.place(x=650)
border_color5.place(x=705, y=90)
border_color6.place(x=824, y=150)
qc_directorydisplay.place(x=630, y=60)
btn1.pack(padx=2,pady=2)
btn6.pack(padx=2,pady=2)
btn2.pack(padx=2,pady=2)
qcbtn1.pack(padx=2,pady=2)
qcbtn6.pack(padx=2,pady=2)
qcbtn2.pack(padx=2,pady=2)
border_color8.place(x=330,y=90)
border_color7.place(x=350,y=10)
subfolderbutton.pack(padx=2,pady=2)
linebutton.pack(padx=2,pady=2)

def ReplaceVmtText():
    global confirmtimer
    global epicvalue
    global search_sub_directories
    global fileslist
    global selected_dir
    global lastdirectory
    global parameters_replacement_list
    global parameters_search_for_list
    confirmtimer.cancel()
    ResetConfirm()
    if replace_entire_line == True:
        ReplaceVmtTextLine()
        return
    if len(selected_dir) <= 3 or len(parameters_replacement_list) <= 0:
        print("No directory selected, or no parameters in replacements file.")
        return
    else:
        close_button.config(state=DISABLED)
        try:
            for w in window.winfo_children():
                if isinstance(w, Button):
                    w.configure(state="disabled")
        except Exception:
            print(f"{w} Can't handle state configurations lol.")
        PutFilesIntoList(lastdirectory)
        for vmtfile in fileslist:
            if vmtfile.endswith(".cfg"):
                with open(vmtfile, mode='r') as file:
                    readfile = file.read()
                    for replacementword in parameters_replacement_list:
                        follower = epicvalue
                        searchedword = parameters_search_for_list[follower + 1]
                        readfile = readfile.replace(searchedword, replacementword, -1)
                        print(searchedword, replacementword)
                        epicvalue = epicvalue + 1
                epicvalue = -1
                with open(vmtfile, mode='w') as file:
                    file.write(readfile)
                file.close()
        fileslist.clear()
        close_button.config(state=ACTIVE)
        for w in window.winfo_children():
            if isinstance(w, Button):
                w.configure(state=ACTIVE)

def ReplaceVmtTextLine():
    global confirmtimer
    global epicvalue
    global search_sub_directories
    global fileslist
    global selected_dir
    global lastdirectory
    global parameters_replacement_list
    global parameters_search_for_list
    confirmtimer.cancel()
    ResetConfirm()
    if len(selected_dir) <= 3 or len(parameters_replacement_list) <= 0:
        print("No directory selected, or no parameters in replacements file.")
        return
    else:
        close_button.config(state=DISABLED)
        try:
            for w in window.winfo_children():
                if isinstance(w, Button):
                    w.configure(state="disabled")
        except Exception:
            print(f"{w} Can't handle state configurations lol.")
        PutFilesIntoList(lastdirectory)
        for vmtfile in fileslist:
            if vmtfile.endswith(".vmt"):
                with open(vmtfile, mode='r') as file:
                    lines = file.readlines()  # Read all lines from the file
                with open(vmtfile, mode='w') as file:
                    for line in lines:
                        for searchedword, replacementword in zip(parameters_search_for_list, parameters_replacement_list):
                            if searchedword in line:
                                # Replace the entire line with the replacementword
                                print(f"Replacing line containing '{searchedword}' with '{replacementword}'")
                                line = replacementword + "\n"
                                break  # Exit the inner loop after finding the word
                        file.write(line)  # Write each (potentially modified) line back to the file
                file.close()
        fileslist.clear()
        close_button.config(state=ACTIVE)
        for w in window.winfo_children():
            if isinstance(w, Button):
                w.configure(state=ACTIVE)


def ReplaceQCText():
    global qcconfirmtimer
    global epicvalue
    global search_sub_directories
    global fileslist
    global qc_selected_dir
    global qc_lastdirectory
    global qc_parameters_replacement_list
    global qc_parameters_search_for_list
    qcconfirmtimer.cancel()
    qcResetConfirm()
    if replace_entire_line == True:
        ReplaceQCTextLine()
        return
    if len(qc_selected_dir) <= 3 or len(qc_parameters_replacement_list) <= 0:
        print("No directory selected, or no parameters in replacements file.")
        return
    else:
        close_button.config(state=DISABLED)
        try:
            for w in window.winfo_children():
                if isinstance(w, Button):
                    w.configure(state="disabled")
        except Exception:
            print(f"{w} Can't handle state configurations lol.")
        PutFilesIntoList(qc_lastdirectory)
        for vmtfile in fileslist:
            if vmtfile.endswith(".qc"):
                with open(vmtfile, mode='r') as file:
                    readfile = file.read()
                    for replacementword in qc_parameters_replacement_list:
                        follower = epicvalue
                        searchedword = qc_parameters_search_for_list[follower + 1]
                        readfile = readfile.replace(searchedword, replacementword, -1)
                        epicvalue = epicvalue + 1
                epicvalue = -1
                with open(vmtfile, mode='w') as file:
                    file.write(readfile)
                file.close()
        fileslist.clear()
        close_button.config(state=ACTIVE)
        for w in window.winfo_children():
            if isinstance(w, Button):
                w.configure(state=ACTIVE)


def ReplaceQCTextLine():
    global epicvalue
    global search_sub_directories
    global fileslist
    global qc_selected_dir
    global qc_lastdirectory
    global qc_parameters_replacement_list
    global qc_parameters_search_for_list
    qcconfirmtimer.cancel()
    qcResetConfirm()
    if len(qc_selected_dir) <= 3 or len(qc_parameters_replacement_list) <= 0:
        print("No directory selected, or no parameters in replacements file.")
        return
    else:
        close_button.config(state=DISABLED)
        try:
            for w in window.winfo_children():
                if isinstance(w, Button):
                    w.configure(state="disabled")
        except Exception:
            print(f"{w} Can't handle state configurations lol.")
        PutFilesIntoList(qc_lastdirectory)
        for vmtfile in fileslist:
            if vmtfile.endswith(".qc"):
                with open(vmtfile, mode='r') as file:
                    lines = file.readlines()  # Read all lines from the file
                with open(vmtfile, mode='w') as file:
                    for line in lines:
                        for searchedword, replacementword in zip(qc_parameters_search_for_list, qc_parameters_replacement_list):
                            if searchedword in line:
                                # Replace the entire line with the replacementword
                                print(f"Replacing line containing '{searchedword}' with '{replacementword}'")
                                line = replacementword + "\n"
                                break  # Exit the inner loop after finding the word
                        file.write(line)  # Write each (potentially modified) line back to the file
                file.close()
        fileslist.clear()
        close_button.config(state=ACTIVE)
        for w in window.winfo_children():
            if isinstance(w, Button):
                w.configure(state=ACTIVE)

# Start the application
if __name__ == "__main__":
    Startup()