import tkinter as tk
from dragFrame import DragFrame
from random import randint


class Display(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('n Points Bézier curve test')
        self.geometry('700x500')

        self.t = 0
        self.reverse = False

        self.create_canvas()
        self.points = self.create_points(4)
        self.clock()


    def clock(self):
        points = [i.get_pos() for i in self.points]

        self.canvas.delete('all')
        self.draw_path(points)

        x, y = self.bezier_curve(self.ease(self.t/100), points)
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


    def draw_path(self, points:tuple | list):
        start = None

        for t in range(0, 16):
            x, y = self.bezier_curve(t/15, points)

            if start is not None:
                self.canvas.create_line(start[0], start[1], x, y, width=4, fill='#c7c7c7')

            start = (x,y)


    def lerp(self, t:float, p0:tuple, p1:tuple) -> tuple:
        x = int((1-t)*p0[0] + t*p1[0])
        y = int((1-t)*p0[1] + t*p1[1])
        return (x, y)


    def bezier_curve(self, t:float, points:tuple | list) -> tuple:
        lines = list()

        if len(points) > 2:
            for i in range(1, len(points)):
                lines.append(self.lerp(t, points[i-1], points[i]))

            while len(lines) > 2:
                lines[0] = self.lerp(t, lines[0], lines[1])
                lines[1] = self.lerp(t, lines[1], lines.pop(2))
            
        else:
            lines = points

        x, y = self.lerp(t, lines[0], lines[1])
        return (x, y)
    

    def create_points(self, n:int = 2) -> list:
        if n <= 1:
            raise Exception("Number of points has to be 2 or higher")

        points = list()

        self.red = DragFrame(self, height=15, width=15, bg='red')
        self.red.place(x=randint(10,200), y=randint(10,490))
        points.append(self.red)

        if n > 2:
            for i in range(n-2):
                black = DragFrame(self, height=15, width=15, bg='black')
                black.place(x=randint(10, 690), y=randint(10,490))
                points.append(black)

        self.green = DragFrame(self, height=15, width=15, bg='green')
        self.green.place(x=randint(500,690), y=randint(10,490))
        points.append(self.green)

        return points


    def create_canvas(self):
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=True, fill='both')
        self.blue = tk.Frame(self, height=15, width=15, bg='blue')


    def ease(self, x:float):
        if x < 0.5:
            t = 8 * x * x * x * x
        else:
            t = 1 - (-2 * x + 2)**4 / 2
        return t


if __name__ == '__main__':
    Display().mainloop()
