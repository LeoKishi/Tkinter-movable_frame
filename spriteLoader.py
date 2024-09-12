import tkinter as tk
from PIL import ImageTk, Image
from typing import Callable


class SpriteSheet:
    def __init__(self, file:str):
        self.img = Image.open(file)


    def get_sprite(self, size:tuple[int, int], position:tuple[int, int]) -> ImageTk.PhotoImage:
        '''
        Returns the sprite at the specified position as a PhotoImage instance.\n
        Arguments:
            size
                tuple containing the height and width of the sprite in pixels
            position
                x,y position of the sprite in the grid
        '''
        height, width = size[0], size[1]
        row, column = position[0], position[1]

        left = width * column
        top = height * row
        right = left + width
        bottom = top + height

        cropped_image = self.img.crop((left, top, right, bottom))
        return ImageTk.PhotoImage(cropped_image)


    def get_sequence(self, size:tuple[int, int], row:int = 1, start:int = 1, stop:int = None) -> list[ImageTk.PhotoImage]:
        '''
        Returns the sprite sequence at the specified row as a list of PhotoImage instances.\n
        Arguments:
            size
                tuple containing the height and width of the sprite in pixels
            row
                which row to be processed
            start
                which sprite to start the sequence
            stop
                which sprite to end the sequence       
        '''
        sequence = []
        height, width = size[0], size[1]

        if not stop:
            stop = self.img.size[0] // width

        for frame in range(start-1, stop):
            left = width * frame
            top = height * (row-1)
            right = left + width
            bottom = top + height

            cropped_image = self.img.crop((left, top, right, bottom))
            sequence.append(ImageTk.PhotoImage(cropped_image))

        return sequence


class Sprite(tk.Label):
    '''
    Custom Tkinter Label class to play animations.\n

    The play( ) method can be used to play a specific sequence or to start the queued animations.\n

    The animation can be stopped at any time with the stop( ) method\n

    Animations can be queued with the chain( ) method.
        If the animation is running, the next sequence plays when 
        the previous one automatically stops or if the next( ) method is called manually.

    '''
    def __init__(self, root:tk.Tk, master:tk.Frame = None, image:tk.PhotoImage = None):
        super().__init__(master, image=image, relief=tk.FLAT, borderwidth=0, highlightthickness=0)

        self.root = root
        self.stop_id = None
        self.queue = list()
    

    def play(self, sequence:list[tk.PhotoImage] = None, loop:bool = False, fps:int = 15, timer:int = None):
        '''Plays the given sequence or the items on queue.'''
        if sequence:
            self.stop()
            self._start_animation(sequence, loop, fps)
            if timer is not None:
                self.root.after(timer, self.next)
        else:
            self.next()


    def next(self):
        '''Jumps to the next item in the queue.'''
        self.stop()

        if not self.queue:
            return

        self._handle_queue()


    def stop(self):
        '''Stops the animation'''
        if self.stop_id:
            self.root.after_cancel(self.stop_id)


    def chain(self, sequence:list[tk.PhotoImage], timer:int = None, loop:bool = False, fps:int = 15):
        '''Adds a animation to the queue.'''
        self.queue.append((sequence, loop, fps, timer))


    def chain_image(self, image:tk.PhotoImage, timer:int = None):
        '''Adds a image to the queue.'''
        self.queue.append((image, timer))


    def chain_func(self, func:Callable, timer:int = None):
        '''Adds a function to the queue.'''
        self.queue.append((func, timer))


    def set_image(self, image:tk.PhotoImage):
        '''Stops any ongoing animation and sets a still image.'''
        self.stop()
        self['image'] = image


    def clear_queue(self):
        '''Removes all queued items.'''
        self.queue = list()


    def _handle_queue(self):
        '''Handles the different types of items in the queue.'''
        item = self.queue[0][0]
        info = self.queue.pop(0)

        # sequence
        if isinstance(item, list):
            self.play(*info[:-1])

        # image
        elif isinstance(item, tk.PhotoImage):
            image = info[0]
            self['image'] = image

        # function
        elif isinstance(item, Callable):
            func = info[0]
            func()

        timer = info[-1]
        if timer is not None:
            self.root.after(timer, self.next)


    def _start_animation(self, sequence:list[tk.PhotoImage], loop:bool, fps:int, _frame:int = 0):
        '''Starts the animation sequence.'''
        self['image'] = sequence[_frame]

        if _frame < len(sequence)-1:
            _frame += 1
        elif loop:
            _frame = 0
        elif self.queue:
            self.next()
            return
        else:
            return

        if self.stop_id:
            self.stop_id = None

        self.stop_id = self.root.after(1000//fps, self._start_animation, sequence, loop, fps, _frame)
