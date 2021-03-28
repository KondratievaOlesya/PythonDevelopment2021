import tkinter as tk
from functools import partial
import re


class Application(tk.Frame):

    def __init__(self, master=None, title="<application>", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        pass


class App(Application):
    def create_text(self):
        self.text = tk.Text(self, undo=True, wrap=tk.WORD)
        self.text.grid(row=0, column=0, sticky="NEWS")
        self.text.bind('<KeyRelease>', self.on_insert_text)

    def create_canvas(self):
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=1, sticky="NEWS")
        self.canvas.bind('<Button-1>', self.canvas_click)
        self.canvas.bind('<Button1-Motion>', self.on_motion)

    def canvas_click(self, event):
        overlap = self.canvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
        if overlap:
            return
        self.create_object(event.x, event.y)
        self.create_row_text()

    def create_row_text(self):
        obj_info = {
            'type': self.canvas.type(self.current_obj),
            'coord': self.canvas.coords(self.current_obj),
            'border_color': self.canvas.itemcget(self.current_obj, 'outline'),
            'fill_color': self.canvas.itemcget(self.current_obj, 'fill'),
            'width': self.canvas.itemcget(self.current_obj, 'width')
        }
        self.text.insert(
            tk.END,
            f'{obj_info["type"]}: <{obj_info["coord"]}> {obj_info["width"]} {obj_info["border_color"]} {obj_info["fill_color"]} \n'
        )

    def create_object(self, x, y):
        self.current_start = x, y
        self.current_end = x + 10, y + 10
        self.current_obj = self.canvas.create_oval(*self.current_start, *self.current_end, fill="white")
        self.canvas.tag_bind(self.current_obj, '<Button-1>', partial(self.object_click, self.current_obj))

    def object_click(self, tag, event):
        self.current_obj_start = event.x, event.y
        self.current_obj_coord = self.canvas.coords(tag)
        self.current_obj = ''
        self.canvas.tag_bind(tag, '<Button1-Motion>', partial(self.object_movement, tag))

    def object_movement(self, tag, event):
        x1, y1, x2, y2 = self.current_obj_coord
        start_x, start_y = self.current_obj_start
        diff_x = event.x - start_x
        diff_y = event.y - start_y

        w, h = self.winfo_width(), self.winfo_height()
        if x1 + diff_x >= 0 and x2 + diff_x <= h and y1 + diff_y >= 0 and y2 + diff_y <= w:
            self.canvas.coords(tag, x1 + diff_x, y1 + diff_y, x2 + diff_x, y2 + diff_y)
            self.change_text(tag, x1 + diff_x, y1 + diff_y, x2 + diff_x, y2 + diff_y)

    def on_motion(self, event):
        overlap = self.canvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
        if overlap:
            return

        # change obj coords
        self.canvas.coords(self.current_obj, *self.current_start, event.x, event.y)

        # change text coords
        self.change_text(self.current_obj, *self.current_start, event.x, event.y)

    def change_text(self, tag, x1, y1, x2, y2):
        if tag == '':
            return
        line = self.text.get(f'{tag}.0', f'{int(tag) + 1}.0')
        s = line.find('<')
        e = line.find('>')
        line = line[:s + 1] + f'{[x1, y1, x2, y2]}' + line[e:]
        self.text.delete(f'{tag}.0', f'{int(tag) + 1}.0')
        self.text.insert(
            f'{tag}.0',
            line
        )

    def on_insert_text(self, event):
        tag = int(self.text.index(tk.INSERT)[:1])
        line = self.text.get(f'{tag}.0', f'{int(tag) + 1}.0')
        configs = line.split(' ')
        line_reg = r'oval: <\[(([0-9]{1,3}|[0-9]{1,3}\.[0-9]{1,2}), ){3}([0-9]{1,3}|[0-9]{1,3}\.[0-9]{1,2})\]> ([0-9]{1,3}\.[0-9]{1,2}) .+\n$'
        try:
            if not re.match(line_reg, line):
                raise Exception('Wrong format!')
            type, x1, y1, x2, y2, width, outline_color, fill_color, new_line = configs
            self.canvas.itemconfig(tag, width=width, outline=outline_color, fill=fill_color)
            self.canvas.coords(tag, x1[2:-1], y1[:-1], x2[:-1], y2[:-2])
            self.text.tag_delete(f'red{tag}.0{int(tag) + 1}.0')
        except Exception as e:
            self.text.tag_add(f'red{tag}.0{int(tag) + 1}.0', f'{tag}.0', f'{int(tag) + 1}.0')
            self.text.tag_configure(f'red{tag}.0{int(tag) + 1}.0', background='red')

    def create_widgets(self):
        self.create_text()
        self.create_canvas()


app = App(title="Graphics Editor")
app.mainloop()
