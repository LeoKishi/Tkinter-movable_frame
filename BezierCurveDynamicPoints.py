import tkinter as tk
from dragFrame import DragFrame
from random import randint


class Display(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Bézier curve movable point test')
        self.geometry('700x500')

        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill='both')

        self.red = DragFrame(self, height=15, width=15, bg='red')
        self.r_pos = (randint(10,200), randint(10,490))
        self.red.place(x=self.r_pos[0], y=self.r_pos[1])

        self.black = DragFrame(self, height=15, width=15, bg='black')
        self.b_pos = (randint(300, 400), randint(10,490))
        self.black.place(x=self.b_pos[0], y=self.b_pos[1])

        self.green = DragFrame(self, height=15, width=15, bg='green')
        self.g_pos = (randint(500,690), randint(10,490))
        self.green.place(x=self.g_pos[0], y=self.g_pos[1])

        self.blue = tk.Frame(self, height=15, width=15, bg='blue')

        self.t = 0
        self.reverse = False

        self.clock()


    def easeInOutQuart(self, x:float):
        if x < 0.5:
            val = 8 * x * x * x * x
        else:
            val = 1 - (-2 * x + 2)**4 / 2
        return val


    def clock(self):
        self.canvas.delete('all')
        self.draw_path()

        t = self.easeInOutQuart(self.t/100)
        x, y = self.equation(self.red.get_pos(), self.black.get_pos(), self.green.get_pos(), t)
        self.blue.place(x=x-7, y=y-7)

        if self.reverse:
            self.t -= 1.5
            if self.t <= 0:
                self.reverse = False
        else:
            self.t += 1.5
            if self.t >= 100:
                self.reverse = True

        self.after(25, self.clock)


    def draw_path(self):
        start = None

        for t in range(0, 16):
            t = t/15
            x, y = self.quadratic_bezier(self.red.get_pos(), self.black.get_pos(), self.green.get_pos(), t)

            if start is not None:
                self.canvas.create_line(start[0], start[1], x, y, width=4, fill='#c7c7c7')

            start = (x,y)


    def quadratic_bezier(self, p0:tuple, p1:tuple, p2:tuple, t:float) -> tuple:
        x = int((1-t)**2*p0[0] + (2*t*(1-t)*p1[0]) + t**2*p2[0])
        y = int((1-t)**2*p0[1] + (2*t*(1-t)*p1[1]) + t**2*p2[1])

        return (x, y)


if __name__ == '__main__':
    Display().mainloop()
