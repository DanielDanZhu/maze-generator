from PIL import Image
import random
import sys

sys.setrecursionlimit(3000)

class Maze:
    def __init__(self, w, h, color, order, factor, save_loc):
        self.wcells, self.hcells = w, h
        self.w, self.h = w * 2 + 1, h * 2 + 1
        self.color, self.factor, self.order, self.save_loc = color, factor, order, save_loc
        self.colors, self.change = [255, 255, 255], [factor] * 3

        self.im = Image.new('RGBA', (self.w, self.h), color = 'black')
        self.pix = self.im.load()

    def generate(self):
        unvisited = []
        if self.color:
            for i in range(len(self.colors)):
                self.colors[i] -= random.randint(0, 255)

        for x in range(self.wcells):
            for y in range(self.hcells):
                unvisited.append([x, y])

        first = random.choice(unvisited)
        self.visit(first[0], first[1], unvisited)

        start_x = random.randint(0, self.wcells - 1) * 2 + 1
        start_y = random.randint(0, self.wcells - 1) * 2 + 1
        self.colors[0], self.colors[1], self.colors[2], none = self.pix[start_x, 1]
        self.color_pix(start_x, 0)
        self.colors[0], self.colors[1], self.colors[2], none = self.pix[start_y, self.h-2]
        self.color_pix(start_y, self.h - 1)

        self.im.save(self.save_loc)
        # if input("enlarged version (y/n): ") == 'y':
        #     self.resize(int(input("factor: ")))

    def visit(self, x, y, unvisited):
        self.color_pix(x * 2 + 1, y * 2 + 1)
        if self.color:
            self.change_colors()
        unvisited.remove([x, y])
        this_colors = [self.colors[0], self.colors[1], self.colors[2]]

        directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        random.shuffle(directions)

        for xdir, ydir in directions:
            xcurr = x + xdir
            ycurr = y + ydir
            if [xcurr, ycurr] in unvisited:
                if self.order:
                    self.colors = [this_colors[0], this_colors[1], this_colors[2]]
                self.color_pix(x * 2 + 1 + xdir, y * 2 + 1 + ydir)
                if self.color:
                    self.change_colors()
                self.visit(xcurr, ycurr, unvisited)

    def color_pix(self, x, y):
        self.pix[x, y] = (self.colors[0], self.colors[1], self.colors[2], 255)

    def change_colors(self):
        for i in range(3):
            if self.colors[i] >= 255:
                self.change[i] = -(self.factor  + (i + 1))
            elif self.colors[i] <= 30:
                self.change[i] = self.factor + (i + 1)
            self.colors[i] += self.change[i]

    def resize(self, factor):
        large_im = Image.new('RGBA', (self.w * factor, self.h * factor), color = 'black')
        large_pix = large_im.load()
        for x in range(large_im.width):
            for y in range(large_im.height):
                large_pix[x, y] = self.pix[int(x / factor), int(y / factor)]
        large_im.save('mazes\mazelarge.png')

def prompt():
    w = int(input("width: "))
    h = int(input("height: "))
    c = input("colored path (y/n): ") == 'y'
    save_loc = "mazes\maze.png"
    if c:
        return Maze(w, h, c, input("based on order of creation (y/n): ") != 'y', int(input("color gradient factor: ")), save_loc)
    return Maze(w, h, c, False, 0, save_loc)

# m = Maze(70, 70, True, False, 1, "mazes\maze.png")
m = prompt()
m.generate()
