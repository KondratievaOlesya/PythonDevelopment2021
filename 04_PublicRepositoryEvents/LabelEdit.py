import tkinter as tk

FONT_WIDTH = 8


class InputLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        # self.label_text = tk.StringVar()
        # self.label_text = kwargs.get('text')
        super().__init__(master, **kwargs)
        self.frame = tk.Frame(self, width=1, bg='black')
        self.frame_placed = False
        self.bind('<Button-1>', self.focus_in)
        self.bind('<Key>', self.key_press)
        self.bind("<FocusOut>", self.focus_release)

    def focus_in(self, event):
        self.config(relief='groove')
        self.focus_set()
        if event.x % FONT_WIDTH != 0:
            text_len = (event.x // FONT_WIDTH + 1) * FONT_WIDTH
        else:
            text_len = event.x

        min_len = len(self.cget("text")) * FONT_WIDTH
        text_len = min_len if min_len == 0 or text_len - min_len > 1 else text_len
        self.frame.place(x=text_len, y=self.winfo_y(), relheight=0.99)
        self.frame_placed = True

    def key_press(self, event):
        if self.frame_placed:
            if char := event.char:
                sign = self.frame.winfo_x() // FONT_WIDTH
                string = self.cget("text")
                new_string = string[:sign] + event.char
                if sign < len(string):
                    new_string += string[sign:]
                self.config(text=new_string)
                self.frame.place(x=self.frame.winfo_x() - 2 + FONT_WIDTH, y=self.winfo_y(), relheight=0.99)
            elif event.keysym == 'Home' or event.keysym == 'Left':
                self.frame.place(x=min(self.frame.winfo_x() - 2 - FONT_WIDTH, len(self.cget("text")) * FONT_WIDTH),
                                 y=self.winfo_y(), relheight=0.99)
            elif event.keysym == 'End' or event.keysym == 'Right':
                self.frame.place(x=min(self.frame.winfo_x() - 2 + FONT_WIDTH, len(self.cget("text")) * FONT_WIDTH),
                                 y=self.winfo_y(), relheight=0.99)
            elif event.keysym == 'Delete':
                sign = self.frame.winfo_x() // FONT_WIDTH
                string = self.cget("text")
                new_string = string[:sign]
                if sign + 1 < len(string):
                    new_string += string[sign + 1:]
                self.config(text=new_string)
                self.frame.place(x=self.frame.winfo_x() - 2, y=self.winfo_y(), relheight=0.99)

    def focus_release(self, event):
        self.config(relief='flat')
        self.frame_placed = False
        self.frame.place(x=0, y=20)


app = tk.Tk()
app.minsize(20, 40)
for column in range(1):
    app.columnconfigure(column, weight=1)
for row in range(2):
    app.rowconfigure(row, weight=1)
label = InputLabel(app, font='TkFixedFont', anchor="w")
label.grid(row=0, column=0, sticky='EW')

quit_button = tk.Button(app, text='Quit', command=app.quit)
quit_button.grid(row=1, column=0)

app.mainloop()
