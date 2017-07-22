import tkinter as tk
import data

data.saveFilesToList()

# creating the root or 'master/parent' window
root = tk.Tk()
app_name = root.title("TakeNote")

# width
window_width = 600

# height
window_height = 400

# windows x position
window_x_pos = int((root.winfo_screenwidth() / 2) - (window_width / 2))

# windows y position
window_y_pos = int((root.winfo_screenheight() / 2) - (window_height / 2))

# using the previous four variables to set the windows dimension and position
root.geometry(str(window_width) + 'x' + str(window_height) + '+' + str(window_x_pos) + '+' + str(window_y_pos))

main_frame = tk.Frame(root)
main_frame.pack()

file_tree_frame = tk.Frame(main_frame, bd=0, highlightthickness=0)
file_tree_frame.pack(side='left', anchor='nw')

file_tree_canvas = tk.Canvas(file_tree_frame, width=150, height=600,
                             highlightthickness=0, bg="#000", scrollregion=(0, 0, 500, 500))
file_tree_canvas.config(width=150, height=600)

horizontal_scrollbar = tk.Scrollbar(file_tree_frame, orient="horizontal")
horizontal_scrollbar.pack(side='bottom', fill='x')
horizontal_scrollbar.config(command=file_tree_canvas.xview)

vertical_scrollbar = tk.Scrollbar(file_tree_frame, orient='vertical')
vertical_scrollbar.pack(side='right', fill='y')
vertical_scrollbar.config(command=file_tree_canvas.yview)

file_tree_canvas.config(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)
file_tree_canvas.pack(side='left', anchor='nw', fill='both', expand=False)

file_tree_button_frame = tk.Frame(file_tree_canvas, width=150, height=400)
file_tree_button_frame.pack(side='left', anchor='nw')


# the configure_interior and the configure_canvas are copied from
# stack overflow to help with the button display with scrolling
def configureInterior(event):
    # update the scrollbars to match the size of the inner frame
    size = (file_tree_button_frame.winfo_reqwidth(), file_tree_button_frame.winfo_reqheight())
    file_tree_canvas.config(scrollregion="0 0 %s %s" % size)
    if file_tree_button_frame.winfo_reqwidth() != file_tree_canvas.winfo_width():
        # update the canvas's width to fit the inner frame
        file_tree_canvas.config(width=file_tree_canvas.winfo_reqwidth())


file_tree_button_window = file_tree_canvas.create_window(0, 0, window=file_tree_button_frame, anchor='nw')

file_tree_button_frame.bind('<Configure>', configureInterior)


def configureCanvas(event):
    if file_tree_button_frame.winfo_reqwidth() != file_tree_canvas.winfo_width():
        # update the inner frame's width to fill the canvas
        file_tree_canvas.itemconfigure(file_tree_button_window, width=file_tree_canvas.winfo_width())


file_tree_canvas.bind('<Configure>', configureCanvas)

file_tree_button_list = []

working_file_page_frame = tk.Frame(main_frame, bd=0, highlightthickness=0)
working_file_page_frame.pack(side='left', anchor='nw')

# Creating working file
working_file = tk.Text(working_file_page_frame, width=600, wrap='word')
working_file.pack(side='bottom', anchor='w', fill='y')

# setting a label to tell user what to enter in the text entry
working_file_name_label = tk.Label(working_file_page_frame, text='File Name:')
working_file_name_label.pack(side='left', anchor='w')

# Creating a string object which helps store the user input
file_name_given_by_user = tk.StringVar()


def saveFile():
    """
    this function helps retrieve the user input using the the
    string object we created in the previous line and then
    outputs the data
    
    :return: 
    """

    working_file_name_given = file_name_given_by_user.get()
    working_file_data = working_file.get(1.0, 'end-1c')

    print('File name: ' + working_file_name_given)
    print('File data: ' + working_file_data)
    print("Done")

    data.updateDataBase(working_file_name_given, working_file_data)

    # add new button if it is a new file
    if data.permissionToCreateButton():
        Btn(working_file_name_given)


# Creating an entry for the user to set the file's name
file_name = tk.Entry(working_file_page_frame, textvariable=file_name_given_by_user)
file_name.pack(side='left', anchor='w')

# Creating this button to save the file and file's name
save_file_btn = tk.Button(working_file_page_frame, text='Save', command=saveFile)
save_file_btn.pack(side='left', anchor='w')


class Btn:
    def __init__(self, f_name):
        self.f_name = f_name
        self.btn = tk.Button(file_tree_button_frame, text=self.f_name)
        self.btn.config(command=lambda: self.callback())
        self.btn.pack()

    def callback(self):
        for file in data.all_files_and_titles:
            if file[0] == self.f_name:
                file_name.delete(0, 'end')
                file_name.insert(0, file[0])

                working_file.delete('1.0', 'end')
                working_file.insert('1.0', file[1])

# Creating all the file tree buttons
for f in data.all_files_and_titles:
    file_btn = Btn(f[0])

# running the app
root.mainloop()

# close off the database
data.closeDataBase()
