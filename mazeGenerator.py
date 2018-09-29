from PIL import Image
import random

class Maze:
    def __init__(self, w, h, c, f):
        self.wcells, self.hcells = w, h
        self.w, self.h = w * 2 + 1, h * 2 + 1
        self.color, self.factor = c, f
        self.colors, self.change = [255, 255, 255], [f] * 3

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

        self.color_pix(random.randint(0, self.wcells - 1) * 2 + 1, 0)
        self.color_pix(random.randint(0, self.wcells - 1) * 2 + 1, self.h - 1)

        self.im.save('maze.png')
        if input("enlarged version (y/n): ") == 'y':
            self.resize(int(input("ratio: ")))

    def visit(self, x, y, unvisited):
        self.color_pix(x * 2 + 1, y * 2 + 1)
        if self.color:
            self.change_colors()
        unvisited.remove([x, y])

        directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        random.shuffle(directions)

        for xdir, ydir in directions:
            xcurr = x + xdir
            ycurr = y + ydir
            if [xcurr, ycurr] in unvisited:
                self.color_pix(x * 2 + 1 + xdir, y * 2 + 1 + ydir)
                if self.color:
                    self.change_colors()
                self.visit(xcurr, ycurr, unvisited)

    def color_pix(self, x, y):
        self.pix[x, y] = (self.colors[0], self.colors[1], self.colors[2], 255)

    def change_colors(self):
        for x in range(3):
            if self.colors[x] >= 255:
                self.change[x] -= self.factor * 2 * (x + 1)
            elif self.colors[x] <= 0:
                self.change[x] += self.factor * 2 * (x + 1)
            self.colors[x] += self.change[x]

    def resize(self, ratio):
        large_im = Image.new('RGBA', (self.w * ratio, self.h * ratio), color = 'black')
        large_pix = large_im.load()
        for x in range(large_im.width):
            for y in range(large_im.height):
                large_pix[x, y] = self.pix[int(x / ratio), int(y / ratio)]
        large_im.save('mazelarge.png')

def prompt():
    w = int(input("width: "))
    h = int(input("height: "))
    c = input("colored path creation (y/n): ") == 'y'
    if c:
        return Maze(w, h, c, int(input("color gradient factor: ")))
    return Maze(w, h, c, 0)

#m = Maze(20, 20, True, 1)
m = prompt()
m.generate()
