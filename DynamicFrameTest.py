import tkinter as tk
from dragFrame import DragFrame
from spriteLoader import Sprite, SpriteSheet


class Display(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Widget drag & drop test')
        self.geometry('700x500')

        self.frame = tk.Frame(self, height=300, width=300, bg='pink')
        self.frame.pack_propagate(0)
        self.frame.pack()

        self.red = DragFrame(self, height=100, width=100, bg='red')
        self.red.pack_propagate(0)
        self.red.pack()

        self.blue = DragFrame(self.frame, height=100, width=50, bg='blue')
        self.blue.pack()

        self.load_sprites()
        self.play_animation()

        self.red.bind_children_widgets()


    def load_sprites(self):
        self.crown = SpriteSheet('assets/crown.png')
        self.red_crown = self.crown.get_sequence(size=(100,100), row=2)


    def play_animation(self):
        self.animation = Sprite(self, self.red)
        self.animation.pack()
        self.animation.play(self.red_crown, loop=True, fps=12)


Display().mainloop()