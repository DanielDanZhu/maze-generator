from PIL import Image
import random

class Maze:
    def __init__(self, w, h):
        self.wcells, self.hcells = w, h
        self.w, self.h = w * 2 + 1, h * 2 + 1

        self.im = Image.new('RGBA', (self.w, self.h), color = 'black')
        self.pix = self.im.load()

    def generate(self):
        unvisited = []

        for x in range(self.wcells):
            for y in range(self.hcells):
                unvisited.append([x, y])

        first = random.choice(unvisited)
        self.visit(first[0], first[1], unvisited)

        startx = random.randint(0, self.wcells - 1)
        endx = random.randint(0, self.wcells - 1)
        self.pix[startx * 2 + 1, 0] = (255, 255, 255, 255)
        self.pix[endx * 2 + 1, self.h - 1] = (255, 255, 255, 255)
        self.im.save('solution.png')
        self.enlarge()

    def visit(self, x, y, unvisited):
        self.pix[x * 2 + 1, y * 2 + 1] = (255, 255, 255, 255)
        unvisited.remove([x, y])

        directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        random.shuffle(directions)

        for xdir, ydir in directions:
            xcurr = x + xdir
            ycurr = y + ydir
            if [xcurr, ycurr] in unvisited:
                self.pix[x * 2 + 1 + xdir, y * 2 + 1 + ydir] = (255, 255, 255, 255)
                self.visit(xcurr, ycurr, unvisited)

    def enlarge(self):
        factor = 20
        #large_im = Image.new('RGBA', (self.w * factor, self.h * factor), color = 'black')
        large_im = self.im.resize((self.w * factor, self.h * factor), Image.ANTIALIAS)
        large_im.save('solutionlarge.png')

w = int(input("width: "))
h = int(input("height: "))
m = Maze(w, h)
m.generate()
