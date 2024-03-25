from tkinter import *
import mysql.connector
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
from tkinter import PhotoImage, scrolledtext, filedialog, messagebox, ttk
from math import ceil, floor
import time

def Image_Manager(photo, x=16, y=16):
    image = Image.open(photo)
    image = image.resize((x, y))
    image = ImageTk.PhotoImage(image)
    return image

def Popup(root):
    popup = Toplevel(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    popup_width = 320
    popup_height = 150
    x_position = (screen_width - popup_width) // 2
    y_position = (screen_height - popup_height) // 2
    popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")
    popup.overrideredirect(True)

    theme = ThemedStyle(popup)
    theme.set_theme('clearlooks')

    frame = Frame(popup, height=35, bg='lightgray')
    frame.pack(side='top')

    label_name = Label(frame, text='Notepad', fg='Black', bg='lightgray', width=6, height=1)
    label_name.pack(padx=0, pady=2, side='left')

    photo_close = Image_Manager('C:/Users/user/Desktop/Python_GUI/images/close.png', x=20, y=20)
    button = Button(frame, image=photo_close, relief='flat', command= lambda: root.destroy())
    button.pack(side='right')

    frame0 = Frame(popup, height=100)
    frame0.pack(side='top')
    address = 'Do you want to close the file/nC:/Users/user/Desktop/Python_/nGUI/images/close.png'
    Label(
        frame0, 
        text=f'{address}', 
        bg='white', 
        fg='blue', 
        height=0, 
        width=40, 
        font=('Helevica', 12),
        anchor='nw'
    ).pack(padx=0, pady=0)

    frame2 = Frame(popup, height=30, bg='lightgray')
    frame2.pack(fill=X, side='bottom')
    ttk.Button(frame2, width=7, text='Cancel').pack(side='right', pady=7, padx=0)
    ttk.Button(frame2, width=10, text="Don't Save").pack(side='right', pady=7, padx=0, command= lambda: root.destroy())
    ttk.Button(frame2, width=5, text='Save').pack(side='right', pady=7, padx=0)

def New(root, message_box):
    text = message_box.get('1.0', END)

    if text.strip()[:-1]:
        var = messagebox.askquestion("Save File", 'Do you want to save changes in Mine?')
        if var == 'yes':
            File_Handling(root, text, 'Save As')

    root.title('Mine - Notepad')
    message_box.delete('1.0', END)

def Path_Setter_For_FH_O(file_path):
    file_path = file_path.split('/')
    path = ''
    for items in file_path[0:-1]:
        path += f'{items}/'

    cursor.execute(f''' UPDATE notepad_  SET rescent_path = '{path}' WHERE ID = 167''')
    connect.commit()

def File_Handling(root, text, title):
    cursor.execute(''' SELECT rescent_path FROM notepad_ WHERE ID = 167 ''')
    info = cursor.fetchall()

    file_path = filedialog.asksaveasfilename(initialdir=info[0][0], title=title, defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
    Path_Setter_For_FH_O(file_path)

    if file_path:
        with open(file_path, 'w') as f:
            f.write(text)
        f.close()

def Open(root, message_box):
    text = message_box.get('1.0', END)

    if text.strip()[:-1]:
        var = messagebox.askquestion("Save File", 'Do you want to save current file?')
        if var == 'yes':
            File_Handling(root, text, 'Open File')
    
    cursor.execute(''' SELECT rescent_path FROM notepad_ WHERE ID = 167 ''')
    info = cursor.fetchall()

    message_box.delete('1.0', END)
    root.filename = filedialog.askopenfilename(initialdir=info[0][0], title='Select a file', filetypes=(("Text File", ".txt") , ("All Files", "*.*")))

    Path_Setter_For_FH_O(root.filename)

    name = (root.filename).split('/')
    name = name[len(name)-1]
    name = name.split('.')
    name = name[0]

    root.title(f'{name} - Notepad')

    try:
        with open(root.filename, 'r') as f:
            line = f.read()
            message_box.insert(INSERT, line) 
        f.close() 
    except Exception:
        pass      

def Undo(root, message_box):
    message_box.event_generate('<<Undo>>')    
    # try:
    #     message_box.edit_undo()
    # except TclError:
    #     pass    

def Cut(root, message_box):
    text = message_box.get(SEL_FIRST, SEL_LAST)
    message_box.delete(SEL_FIRST, SEL_LAST)
    root.clipboard_clear()
    root.clipboard_append(text)

def Copy(root, message_box):
    text = message_box.get(SEL_FIRST, SEL_LAST)
    root.clipboard_clear()
    root.clipboard_append(text)

def Paste(root, message_box):
    text = root.clipboard_get()
    message_box.insert(INSERT, text)

def Delete(root, message_box):
    message_box.delete(SEL_FIRST, SEL_LAST)

def WordWrap(message_box):
    cursor.execute(''' SELECT word_wrap FROM notepad_ ''')
    Info = cursor.fetchall()
    
    if Info[0][0] == 'word':
        cursor.execute(''' UPDATE notepad_ SET word_wrap = 'char' WHERE ID = 167''')
        message_box.config(wrap='char')
    elif Info[0][0] == 'char':
        cursor.execute(''' UPDATE notepad_ SET word_wrap = 'none' WHERE ID = 167''')
        message_box.config(wrap='none')
    elif Info[0][0] == 'none':
        cursor.execute(''' UPDATE notepad_ SET word_wrap = 'word' WHERE ID = 167''')
        message_box.config(wrap='word')
    
    connect.commit()  

def StatusBar(frame_statusBar):
    cursor.execute(''' SELECT status_bar FROM notepad_ ''')
    Info = cursor.fetchall()
    
    if Info[0][0] == 'yes':
        cursor.execute(''' UPDATE notepad_ SET status_bar = 'no' WHERE ID = 167''')
        frame_statusBar.pack_forget()
    else:
        cursor.execute(''' UPDATE notepad_ SET status_bar = 'yes' WHERE ID = 167''')
        frame_statusBar.pack(fill=X, side='top')

    connect.commit()

def Select_All(message_box):
    message_box.tag_add(SEL, "1.0", END)
    message_box.mark_set(SEL_FIRST, "1.0")
    message_box.mark_set(SEL_LAST, END)

def Replace_Process(destination, source, message_box, flag=False):
    print(destination, source)
    search_term = destination

    try:
        if search_term:
            message_box.tag_remove("match", "1.0", END)
            starting_index = "1.0"

            while True:
                start_index = message_box.search(search_term, starting_index, END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(search_term)}c"
                message_box.tag_add(SEL, start_index, end_index)
                message_box.tag_add("match", start_index, end_index)

                message_box.delete(start_index, end_index)
                message_box.insert(start_index, source)

                starting_index = end_index 
                if flag:
                    break

    except Exception as e:
        print(e)  

def Replace(message_box, root):
    popup = Toplevel(root)
    popup.geometry('366x143')
    popup.title('Replace')
    popup.attributes('-toolwindow', True)

    theme = ThemedStyle(popup)
    theme.set_theme('plastik')
        
    value = StringVar()

    text_find = Message(popup, text="Find what: ", font=("Arial", 9), width=100)
    text_find.grid(pady=5, padx=0, column=0, row=0)
    search1 = ttk.Entry(popup, width=30)
    search1.grid(pady=5, padx=1, column=1, row=0)
    button_find = ttk.Button(popup, text=' Find Next', width=10, command=lambda: Get_Entry(search1, message_box))
    button_find.grid(pady=5, padx=10, column=2, row=0)

    text_replace = Message(popup, text="Replace with: ", font=("Arial", 9), width=100)
    text_replace.grid(pady=0, padx=0, column=0, row=1)
    search2 = ttk.Entry(popup, width=30)
    search2.grid(pady=0, padx=1, column=1, row=1)
    button_replace = ttk.Button(popup, text=' Replace', width=10, command=lambda: Replace_Process(search1.get(), search2.get(), message_box, True))
    button_replace.grid(pady=0, padx=10, column=2, row=1)

    button_replaceAll = ttk.Button(popup, text=' Replace All', width=10, command=lambda: Replace_Process(search1.get(), search2.get(), message_box))
    button_replaceAll.grid(pady=5, padx=10, column=2, row=2)

    button_cancel = ttk.Button(popup, text=' Cancel', width=10, command=lambda: popup.destroy())
    button_cancel.grid(pady=0, padx=10, column=2, row=3)

    ttk.Checkbutton(popup, text='Match case').grid(row=3, column=0, padx=0, pady=1)
    ttk.Checkbutton(popup, text='Wrap Word').grid(row=4, column=0, padx=0, pady=1)

def Get_Entry(search, message_box):
    search_term = search.get()
    
    if search_term:
        start_index = "1.0"
        message_box.tag_remove("match", "1.0", END)

        while True:
            index = message_box.search(search_term, start_index, END)
            if not index:
                break
            end_index = f"{index}+{len(search_term)}c"
            message_box.tag_add(SEL, index, end_index)
            message_box.tag_add("match", index, end_index)
            start_index = end_index

        if not message_box.tag_ranges("match"):
            messagebox.showinfo("Notepad",f"Cannot found '{search_term}'")        

def Search(message_box, root):
    popup = Toplevel(root)
    popup.geometry('357x110')
    popup.title('Find')
    popup.attributes('-toolwindow', True)

    theme = ThemedStyle(popup)
    theme.set_theme('plastik')
        
    value = StringVar()

    text_message = Message(popup, text="Find What: ", font=("Arial", 9), width=100)
    text_message.grid(pady=5, padx=0, column=0, row=0)

    search = ttk.Entry(popup, width=30)
    search.grid(pady=5, padx=1, column=1, row=0, columnspan=2)

    button_find = ttk.Button(popup, text=' Find Next', width=10, command=lambda: Get_Entry(search, message_box))
    button_find.grid(pady=5, padx=10, column=3, row=0)

    label_direction = ttk.LabelFrame(popup, text='Direction')
    label_direction.grid(pady=1, padx=0, column=2, row=1, rowspan=2)

    button_cancel = ttk.Button(popup, text='  Cancel', width=10, command=lambda: popup.destroy())
    button_cancel.grid(pady=1, padx=10, column=3, row=1)

    ttk.Radiobutton(label_direction, text='Up').grid(row=0, column=0, padx=0, pady=0)
    ttk.Radiobutton(label_direction, text='Down').grid(row=0, column=1, padx=0, pady=0)

    ttk.Checkbutton(popup, text='Match case').grid(row=2, column=0, padx=0, pady=1)
    ttk.Checkbutton(popup, text='Wrap Word').grid(row=3, column=0, padx=0, pady=1) 

def Zoom_In(message_box):
    cursor.execute(''' SELECT current_font FROM notepad_ ''')
    font = cursor.fetchall()

    percentage = (font[0][0]/100)*10
    new_font = floor(font[0][0] + percentage)

    message_box.configure(font=('Helvetica', new_font))
    cursor.execute(f''' UPDATE notepad_ SET current_font = {new_font} WHERE current_font = {font[0][0]}''')

def Zoom_Out(message_box):
    cursor.execute(''' SELECT current_font FROM notepad_ ''')
    font = cursor.fetchall()

    percentage = (font[0][0]/100)*10
    new_font = floor(font[0][0] - percentage)

    message_box.configure(font=('Helvetica', new_font))
    cursor.execute(f''' UPDATE notepad_ SET current_font = {new_font} WHERE current_font = {font[0][0]}''')

def Orignal_Zoom(message_box):
    cursor.execute(''' SELECT new_font FROM notepad_ ''')
    font = cursor.fetchall()
    message_box.configure(font=('Helvetica', font[0][0]))

def FONT_INFORMATION_DB():
    font, font_style, font_size = [], [], []
    cursor.execute(' SELECT * FROM notepad_fonts')
    Data = cursor.fetchall()
    for value in Data:
        font.append(value[0])
        if value[1] != '/':
            font_style.append(value[1])
        font_size.append(value[2])

    return font, font_style, font_size    

def on_vertical_scroll(canvas, *arg):
    canvas.yview(*arg)

def Font_Setup(entry_1, entry_2, entry_3, index):
    global trigger_msgBox
    trigger_msgBox = True    
    font, font_style = entry_1.get(), entry_2.get()

    if font:
        cursor.execute(f''' UPDATE notepad_ SET font_name = "{font}"  WHERE ID = 167''')
    if font_style:
        cursor.execute(f''' UPDATE notepad_ SET font_style = "{font_style}"  WHERE ID = 167''')
        
    if len(index) == 1:
        font_size =  entry_3.get(index[0])
        cursor.execute(f''' UPDATE notepad_ SET new_font = {font_size}  WHERE ID = 167''')
    
def Fonts(message_box, root):
    global sample_label, font, font_style, font_size
    popup = Toplevel(root)

    popup.geometry('470x500')
    popup.title('Find')
    popup.attributes('-toolwindow', True)

    theme = ThemedStyle(popup)
    theme.set_theme('clearlooks')
    
    frame = Frame(popup)
    frame.grid(padx=10, pady=10, row=0, column=0, rowspan=3)
    frame_ = Frame(popup)
    frame_.grid(padx=10, pady=10, row=0, column=1, rowspan=3)

    frame1 = Frame(frame, bg='gray', padx=1, pady=1)
    frame1.grid(row=2, column=0)

    frame2 = Frame(frame_, bg='gray', padx=1, pady=1)
    frame2.grid(row=2, column=0)

    frame3 = Frame(popup)
    frame3.grid(column=2, row=0, padx=14, pady=10)

    Label(frame, text='Font:', width=22, anchor='nw').grid(row=0, column=0, sticky='w')
    Label(frame_, text='Font Style:', width=12, anchor='nw').grid(row=0, column=0, sticky='w')
    Label(frame3, text='Size:', width=7, anchor='nw').grid(row=0, column=2, sticky='w')

    entry_1 = ttk.Entry(frame, width=15)
    entry_2 = ttk.Entry(frame_, width=15)
    entry_3 = ttk.Entry(frame3, width=10)

    entry_1.grid(row=1, column=0, sticky='we')
    entry_2.grid(row=1, column=0, sticky='we')
    entry_3.grid(row=1, column=2, sticky='we')

    font, font_style, font_size = FONT_INFORMATION_DB()


    canvas = Canvas(frame1, height=130, width=150)
    canvas.grid(sticky='e')

    canvas_frame = Frame(canvas, height=100)
    canvas.create_window((0,0), window=canvas_frame, anchor='nw')

    vertical_scrollbar = Scrollbar(frame1, orient='vertical', command=lambda *args: on_vertical_scroll(canvas, *args))
    vertical_scrollbar.grid(column=1, row=0, sticky='nsw')
    canvas.config(yscrollcommand=vertical_scrollbar.set)

    for i, fonts in enumerate(font):
        Button(
            canvas_frame, 
            text=fonts, 
            font=(fonts, 11),
            height=1, 
            width=18, 
            borderwidth=0, 
            anchor='nw', 
            bg='white',
            command= lambda arg=fonts: entry(entry_1, arg)
        ).grid(row=i+2, column=0,sticky='we')

    canvas_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))


    canvas2 = Canvas(frame2, height=130, width=120)
    canvas2.grid(sticky='e')

    canvas_frame = Frame(canvas2, height=100)
    canvas2.create_window((0,0), window=canvas_frame, anchor='nw')

    vertical_scrollbar = Scrollbar(frame2, orient='vertical', command=lambda *args: on_vertical_scroll(canvas2, *args))
    vertical_scrollbar.grid(column=1, row=0, sticky='nsw')
    canvas2.config(yscrollcommand=vertical_scrollbar.set)

    for i, fonts in enumerate(font_style):
        Button(
            canvas_frame, 
            text=fonts, 
            font=('Arial', 11, fonts), 
            width=18, 
            borderwidth=0,
            anchor='nw', 
            bg='white',
            command= lambda arg=fonts: entry(entry_2, arg)
        ).grid(row=i+2, column=0,sticky='we')

    canvas_frame.update_idletasks()
    canvas2.config(scrollregion=canvas2.bbox('all'))


    list_3 = Listbox(frame3, selectmode=SINGLE, height=5, width=7, font=5)
    list_3.insert(END, *font_size)
    list_3.grid(row=2, column=2)
    scrollbar = Scrollbar(frame3, command=list_3.yview)
    scrollbar.grid(row=2, column=2, sticky='nse')
    list_3.config(yscrollcommand=scrollbar.set)


    cursor.execute(''' SELECT font_name, new_size, font_style FROM notepad_ ''')
    Data = cursor.fetchall()
    fontname = Data[0][0]
    newsize = Data[0][1]
    fontstyle = Data[0][2]

    sample_frame = ttk.LabelFrame(popup, text='Sample', width=10, height=3)
    sample_frame.grid(row=3, column=1, columnspan=2, sticky='nw', padx=5, pady=5)

    sample_label = Label(sample_frame, text='AaBbXxYy', font=(fontname, newsize, fontstyle), width=10, height=3)
    sample_label.grid(sticky='new')

    ok_btn = ttk.Button(popup, text='OK', width=10, command=lambda: Font_Setup(entry_1, entry_2, list_3, list_3.curselection())).grid(row=4, column=1, sticky='ne', padx=10, pady=100)
    cancel_btn = ttk.Button(popup, text='Cancel', width=10, command=lambda: popup.destroy()).grid(row=4, column=2, sticky='nw', padx=10, pady=100)

def entry(entry, value):
    global sample_label, font, font_style, font_size

    if value in font:
        cursor.execute(f''' UPDATE notepad_ SET font_name = '{value}' WHERE ID = 167''')
    elif value in font_style:    
        cursor.execute(f''' UPDATE notepad_ SET font_style = '{value}' WHERE ID = 167''')
    elif value in font_size:    
        cursor.execute(f''' UPDATE notepad_ SET new_size = {value} WHERE ID = 167''')

    cursor.execute(''' SELECT font_name, new_size, font_style FROM notepad_ ''')
    Data = cursor.fetchall()
    fontname = Data[0][0]
    newsize = Data[0][1]
    fontstyle = Data[0][2]

    entry.delete(0, END)
    entry.insert(0, value)
    sample_label.config(font=(fontname, newsize, fontstyle))

    connect.commit()
    
def Time_Date(message_box):
    message_box.insert(END, time.ctime())

def drag_start(event):
    shape = event.widget
    shape.startX = event.x
    shape.startY = event.y

def drag_motion(event):
    shape = event.widget
    x = shape.winfo_x() - shape.startX + event.x
    y = shape.winfo_y() - shape.startY + event.y

    shape.place(x=x, y=y)

def Canvas_Image_Popup(root, message_box):
    popup = Toplevel(root)
    popup.geometry('500x200')
    theme = ThemedStyle(popup)
    theme.set_theme('plastik')

    Label(popup, text='Select Image :', anchor='nw').grid(row=0, column=0, padx=10, pady=10, sticky='w')
    image_path = ttk.Entry(popup, width=50)
    image_path.grid(row=0, column=1, columnspan=5)
    open_button = ttk.Button(popup, text='Open', command= lambda: Canvas_Image(image_path, root))
    open_button.grid(row=0, column=7, padx=10)

    Label(popup, text='Image Size :', anchor='nw').grid(row=1, column=0, padx=10, pady=10, sticky='w')
    Label(popup, text='X :', anchor='nw').grid(row=1, column=1, pady=10, sticky='e')
    image_x = ttk.Entry(popup, width=10)
    image_x.grid(row=1, column=2, sticky='w')
    Label(popup, text='Y :', anchor='nw').grid(row=1, column=3, pady=10, sticky='e')
    image_y = ttk.Entry(popup, width=10)
    image_y.grid(row=1, column=4, sticky='w')

    Label(popup, text='Image Position :', anchor='nw').grid(row=2, column=0, padx=10, pady=10, sticky='w')
    Label(popup, text='X :', anchor='nw').grid(row=2, column=1, pady=10, sticky='e')
    x_position = ttk.Entry(popup, width=10)
    x_position.grid(row=2, column=2, sticky='w')
    Label(popup, text='Y :', anchor='nw').grid(row=2, column=3, pady=10, sticky='e')
    y_position = ttk.Entry(popup, width=10)
    y_position.grid(row=2, column=4, sticky='w')

    option_var = StringVar()
    Label(popup, text='Image Status :', anchor='nw').grid(row=3, column=0, padx=10, pady=10, sticky='w')
    box = ttk.Combobox(popup, textvariable=option_var, values=['Moveable', 'Static'], width=20).grid(row=3, column=1, columnspan=2, pady=10, sticky='w')

    done_button = ttk.Button(popup, text='Done', command=lambda: image_(image_x.get(), image_y.get(), x_position.get(), y_position.get(), image_path.get(), option_var.get(), message_box, popup))
    done_button.grid(row=3, column=7, padx=10, sticky='ew')

def Canvas_Image(image_path, root):
    cursor.execute(''' SELECT rescent_path FROM notepad_ WHERE ID = 167 ''')
    info = cursor.fetchall()
    root.filename = filedialog.askopenfilename(initialdir=info[0][0], title='Select a file', filetypes=(("PNG File", ".png") , ("All Files", "*.*")))
    name = root.filename
    image_path.insert(0, name)

def Popup_Review(root): #event
    # popup = Toplevel()
    popup = root
    popup.geometry('40x75')

    Button(popup, text='Refactor Image', width=15, borderwidth=0, anchor='nw').pack(padx=2, pady=2)
    Button(popup, text='Replace Image', width=15, borderwidth=0, anchor='nw').pack(padx=2, pady=2)
    Button(popup, text='Delete', width=15, borderwidth=0, anchor='nw').pack(padx=2, pady=2)

def image_(x, y, x_loc, y_loc, image_path, option_var, message_box, popup):
    image_new = Image_Manager(f'{image_path}', x=int(x), y=int(y))
    
    image_label = Label(message_box, image=image_new, bg='white')
    image_new.image = image_new
    image_label.place(x=int(x_loc), y=int(y_loc))

    print(option_var)
    if option_var == 'Moveable':
        image_label.bind('<Button-1>', drag_start)
        image_label.bind('<B1-Motion>', drag_motion)

    image_label.bind('<Button-3>', Popup_Review)
    popup.destroy()

def AboutNotepad(root):
    popup = Toplevel(root)

    popup.geometry('440x200')
    popup.title('About')
    popup.attributes('-toolwindow', True)

    theme = ThemedStyle(popup)
    theme.set_theme('clearlooks')
    
    frame = LabelFrame(popup, text="About Notepad", fg="black")
    Label(
        frame, 
        text='''Welcome to Mine - Notepad \n
        This notepad was created by Fizza Nawaz (a BCS Student) in Dec 2023, 
        as a project for practice. This is a simple notepad with a unique 
        function that it can get images. The image can be floatable or can be 
        static depending on choice you make.        
        ''', 
        width=60,
        height=10
    ).grid(row=1)
    frame.grid(column=0, row=0,padx=5, pady=5)

connect = mysql.connector.connect(
    host = 'localhost',
    password = '',
    user = 'root',
    database = 'Notepad'
)   

def BreakConnections():
    cursor.close()
    connect.close()
  
connect.commit()   
cursor = connect.cursor()
cursor.execute('USE Notepad')