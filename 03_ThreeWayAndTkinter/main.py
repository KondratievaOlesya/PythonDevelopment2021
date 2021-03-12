import tkinter as tk
from tkinter import messagebox
import random

PADDING = 5
N = 4
BUTTON_WIDTH = 4
BUTTON_HEIGHT = 2


class Application(tk.Tk):
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        self.game_frame = tk.Frame(self)
        self.buttons_frame = tk.Frame(self)
        self.buttons = []
        self.game_list = []
        self.new_game()

    def is_game_correct(self):
        """ Find out if placement of buttons is correct """
        n = [0 for i in range(N * N)]
        e = 0
        for i in range(N * N):
            if self.game_list[i] == 0:
                e = i // N + 1
            else:
                k = 0
                for j in range(i, N * N):
                    if self.game_list[j] < self.game_list[i] and self.game_list[j] != 0:
                        k += 1
                n[self.game_list[i]] = k
        N_sum = sum(n) + e
        return N_sum % 2 == 0

    def win(self):
        """Find out if game in win state. Show message box if so"""
        for i in range(N * N - 1):
            if self.game_list[i] != i + 1:
                return False
        messagebox.showinfo("15 puzzle", "You won!")
        self.new_game()

    def new_game(self):
        """ Start game """
        self.game_list = [i for i in range(N * N)]
        random.shuffle(self.game_list)
        while not self.is_game_correct():
            random.shuffle(self.game_list)
        self.clear_all()
        self.build_game()

    def clear_all(self):
        """ Destroy buttons from game frame """
        for button in self.buttons:
            button.destroy()

    def move_button(this, id):
        """ Create function to move button with index id to empty space """
        def wrapper(self=this, idx=id):
            right_button = idx + 1 if idx % N != N - 1 else None
            left_button = idx - 1 if idx % N != 0 else None
            top_button = ((idx // N) - 1) * N + (idx % N) if idx // N != 0 else None
            bot_button = ((idx // N) + 1) * N + (idx % N) if idx // N != N - 1 else None
            sides = [right_button, left_button, top_button, bot_button]
            for side in sides:
                if side is not None and self.game_list[side] == 0:
                    self.game_list[side] = self.game_list[idx]
                    self.game_list[idx] = 0
                    self.clear_all()
                    self.build_game()
                    self.win()
                    return

        return wrapper

    def build_game(self):
        """ Creates buttons on game field. """
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Exit and New buttons
        self.buttons_frame.grid(row=0, column=0, sticky='NSEW')
        new_button = tk.Button(self.buttons_frame, text='New', command=self.new_game)
        exit_button = tk.Button(self.buttons_frame, text='Exit', command=self.quit)

        self.buttons_frame.grid_rowconfigure(0, weight=1, pad=PADDING)
        self.buttons_frame.grid_columnconfigure(0, weight=1, pad=PADDING)
        self.buttons_frame.grid_columnconfigure(1, weight=1, pad=PADDING)
        new_button.grid(column=0, row=0, sticky='NSEW')
        exit_button.grid(column=1, row=0, sticky='NSEW')

        # Game field buttons
        self.game_frame.grid(row=1, column=0, columnspan=4, sticky='NSEW')

        for i in range(N):
            self.game_frame.grid_rowconfigure(i, weight=1, pad=PADDING)

        for i in range(N):
            self.game_frame.grid_columnconfigure(i, weight=1, pad=PADDING)

        self.buttons = []
        for i in range(N * N):
            if self.game_list[i] != 0:
                self.buttons.append(
                    tk.Button(self.game_frame,
                              text=f'{self.game_list[i]}',
                              width=BUTTON_WIDTH,
                              height=BUTTON_HEIGHT,
                              command=self.move_button(i)
                    )
                )
                self.buttons[-1].grid(row=i // N, column=i % N, sticky='NSEW')


app = Application()
app.title('15 puzzle')
app.mainloop()
