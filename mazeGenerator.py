from PIL import Image
import random

class Maze:
    def __init__(self, w, h, c, f):
        self.wcells, self.hcells = w, h
        self.w, self.h = w * 2 + 1, h * 2 + 1
        self.color, self.factor = c, f

        self.im = Image.new('RGBA', (self.w, self.h), color = 'black')
        self.pix = self.im.load()

    def generate(self):
        unvisited, change = [], [self.factor] * 3
        colors = [255, 255, 255]
        if self.color:
            for i in range(len(colors)):
                colors[i] -= random.randint(0, 255)

        for x in range(self.wcells):
            for y in range(self.hcells):
                unvisited.append([x, y])

        first = random.choice(unvisited)
        self.visit(first[0], first[1], unvisited, colors, change)

        self.pix[random.randint(0, self.wcells - 1) * 2 + 1, 0] = (colors[0], colors[1], colors[2], 255)
        self.pix[random.randint(0, self.wcells - 1) * 2 + 1, self.h - 1] = (colors[0], colors[1], colors[2], 255)

        self.im.save('solution.png')
        # self.resize()

    def visit(self, x, y, unvisited, colors, change):
        self.pix[x * 2 + 1, y * 2 + 1] = (colors[0], colors[1], colors[2], 255)
        if self.color:
            self.changeColors(colors, change)
        unvisited.remove([x, y])

        directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        random.shuffle(directions)

        for xdir, ydir in directions:
            xcurr = x + xdir
            ycurr = y + ydir
            if [xcurr, ycurr] in unvisited:
                self.pix[x * 2 + 1 + xdir, y * 2 + 1 + ydir] = (colors[0], colors[1], colors[2], 255)
                if self.color:
                    self.changeColors(colors, change)
                self.visit(xcurr, ycurr, unvisited, colors, change)

    def changeColors(self, colors, change):
        for x in range(3):
            if colors[x] >= 255:
                change[x] -= self.factor * 2
            elif colors[x] <= 0:
                change[x] += self.factor * 2
            colors[x] += change[x]

    def resize(self):
        factor = 50
        large_im = Image.new('RGBA', (self.w * factor, self.h * factor), color = 'black')
        large_pix = large_im.load()
        for x in range(large_im.width):
            for y in range(large_im.height):
                large_pix[x, y] = self.pix[int(x / factor), int(y / factor)]
        large_im.save('solutionlarge.png')

w = int(input("width: "))
h = int(input("height: "))
m = Maze(w, h, True, 10)
m.generate()
