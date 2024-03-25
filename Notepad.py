from tkinter import *
from tkinter import ttk, scrolledtext, Scrollbar, PhotoImage
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
from Notepad_Backend import *
from math import floor

root = Tk()
root.title('Notepad | Mine')
root.geometry('756x450')
root.minsize(500, 0)
image = Image_Manager('note.png')
root.iconphoto(True, image)

theme = ThemedStyle(root)
theme.set_theme('plastik')

countChar, countLines = 1, 1

def MenuBar():
    global message_box
    global frame_statusBar

    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    edit_menu = Menu(menu_bar, tearoff=0)
    format_menu = Menu(menu_bar, tearoff=0)
    view_menu = Menu(menu_bar, tearoff=0)
    help_menu = Menu(menu_bar, tearoff=0)
    zoom_menu = Menu(menu_bar, tearoff=0)

    zoom_menu.add_command(label='Zoom in'.ljust(40), command=lambda: Zoom_In(message_box))
    zoom_menu.add_command(label='Zoom out', command=lambda: Zoom_Out(message_box))
    zoom_menu.add_command(label='Restore default zoom', command=lambda: Orignal_Zoom(message_box))

    file_menu.add_command(label='New'.ljust(40), command=lambda: New(root, message_box))
    file_menu.add_command(label='Open', command=lambda: Open(root, message_box))
    file_menu.add_command(label='Insert Image', command=lambda: Canvas_Image_Popup(root, message_box))
    file_menu.add_command(label='Save', command= lambda: File_Handling(root, message_box.get('1.0', END), 'Save'))
    file_menu.add_command(label='Save as', command= lambda: File_Handling(root, message_box.get('1.0', END), 'Save As'))
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=lambda: root.destroy())

    edit_menu.add_command(label='Undo'.ljust(40), command=lambda: message_box.event_generate('<<Undo>>'))
    edit_menu.add_separator()
    edit_menu.add_command(label='Cut', command=lambda: message_box.event_generate('<<Cut>>'))
    edit_menu.add_command(label='Copy', command=lambda: message_box.event_generate('<<Copy>>'))
    edit_menu.add_command(label='Paste', command=lambda: message_box.event_generate('<<Paste>>'))
    edit_menu.add_command(label='Delete', command=lambda: message_box.delete(SEL_FIRST, SEL_LAST))
    edit_menu.add_separator()
    edit_menu.add_command(label='Find', command=lambda: Search(message_box, root))
    edit_menu.add_command(label='Replace...', command=lambda: Replace(message_box, root))
    edit_menu.add_command(label='Go to...')
    edit_menu.add_separator()
    edit_menu.add_command(label='Select all', command=lambda: Select_All(message_box))
    edit_menu.add_command(label='Time/Date', command=lambda: Time_Date(message_box))

    format_menu.add_command(label='Word Wrap'.ljust(40), compound=LEFT, command=lambda: WordWrap(message_box))
    format_menu.add_command(label='Font', command=lambda: Fonts(message_box, root))

    view_menu.add_cascade(label='Zoom'.ljust(30), menu=zoom_menu)
    view_menu.add_command(label='Status bar', compound=LEFT, command=lambda: StatusBar(frame_statusBar))

    help_menu.add_command(label='View help'.ljust(40))
    help_menu.add_command(label='Send Feedback')
    help_menu.add_separator()
    help_menu.add_command(label='About Notepad', command=lambda: AboutNotepad(root))

    menu_bar.add_cascade(label='File', menu=file_menu)
    menu_bar.add_cascade(label='Edit', menu=edit_menu)
    menu_bar.add_cascade(label='Format', menu=format_menu)
    menu_bar.add_cascade(label='View', menu=view_menu)
    menu_bar.add_cascade(label='Help', menu=help_menu)

    root.config(menu=menu_bar)

def update_horizontal_scroll(*args):
    global message_box
    message_box.xview(*args)

def MessageBox():
    global message_box
    cursor.execute(''' SELECT word_wrap, new_font, font_name, font_style FROM notepad_ ''')
    msgbox_info = cursor.fetchall()
        
    message_box = scrolledtext.ScrolledText(root, width=40, height=0, font=(msgbox_info[0][2], msgbox_info[0][1], msgbox_info[0][3]), borderwidth=0)      # wrap='char'
    
    horizontal_scrollbar = Scrollbar(root, orient="horizontal", command=update_horizontal_scroll)
    message_box.config(xscrollcommand=horizontal_scrollbar.set)
    message_box.pack(fill="both", expand=True)
    horizontal_scrollbar.pack(fill="x")

    if msgbox_info[0][0] == 'word':
        message_box.config(wrap='word')
    elif msgbox_info[0][0] == 'char':
        message_box.config(wrap='char')
    else:    
        message_box.config(wrap='none')

    message_box.pack(expand=True, fill='both', side='top') 
    message_box.bind("<KeyRelease>", UpdateStatusBar) 

def UpdateStatusBar(event):
    global message_box, frame_statusBar, label4

    cursor_pos = message_box.index(CURRENT)

    char = message_box.get('1.0', END)
    line = cursor_pos.split('\n')

    status_text = f'Line {floor(float(line[0]))}, Col {str(len(char)-int(len(line)))}'
    label4.config(text=status_text)

def PressKey(event):
    global countChar, countLines, message_box

    text = message_box.get('1.0', END)
    label4.configure(text=f'Line {countLines}, Col {countChar}')

def Enter(event):
    global countChar, countLines, message_box

    text = message_box.get('1.0', END)
    label4.configure(text=f'Line {countLines}, Col {countChar}')

def Status_Bar():
    global frame_statusBar, label4
    frame_statusBar = Frame(root, bg='lightgray')

    cursor.execute(''' SELECT status_bar FROM notepad_ ''')
    Info = cursor.fetchall()
    if Info[0][0] == 'yes':
        frame_statusBar.pack(side='bottom', fill=X)

    sizegrip = ttk.Sizegrip(frame_statusBar)
    sizegrip.pack(side="right", anchor="se")

    label1 = Label(frame_statusBar, text='UTF-8', height=1, width=15, borderwidth=2, bg='lightgray', relief='flat')
    label1.pack(side='right')

    label2 = Label(frame_statusBar, text='Window (CRLF)', height=1, width=20, borderwidth=2, bg='lightgray', relief='flat')
    label2.pack(side='right')

    label3 = Label(frame_statusBar, text='100', height=1, width=7, borderwidth=2, bg='lightgray', relief='flat')
    label3.pack(side='right')

    label4 = Label(frame_statusBar, text='Line 1, Col 1', height=1, width=15, borderwidth=2, bg='lightgray', relief='flat')
    label4.pack(side='right')

MenuBar()
MessageBox()
Status_Bar()

print("before", trigger_msgBox)
if trigger_msgBox == True:
    MessageBox()
    print("before", trigger_msgBox)
    trigger_msgBox = False
    print(trigger_msgBox)

def On_Close():
    connect.commit()
    cursor.close()
    connect.close()
    root.destroy()

root.protocol('WM_DELETE_WINDOW', On_Close)
root.mainloop()