import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        x, y = self.pos

        if x + dirnx < 0:
            x = self.rows - 1
        elif x + dirnx > self.rows - 1:
            x = 0

        if y + dirny < 0:
            y = self.rows - 1
        elif y + dirny > self.rows - 1:
            y = 0

        self.pos = (x + dirnx, y + dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # Width/Height of each cube
        i = self.pos[0]  # Current row
        j = self.pos[1]  # Current Column

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        # By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it

        if eyes:  # Draws the eyes
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0 #direction for x
        self.dirny = 1 #direction for y

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): #for each object position
            p = c.pos[:] #grab the cube position
            if p not in [x[:] for x in self.turns]:
                #checking if we hit the edge of the square
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirnx == -1 and c.pos[0] >= c.rows-1: c.pos = ( c.pos[0],0)
                elif c.dirnx == -1 and c.pos[0] <= 0: c.pos = ( c.pos[0], c.rows-1)
                else: c.move(c.dirnx,c.dirny)

            else:  #see if it is in the turn list
                turn = self.turns[p] #the move
                c.move(turn[0],turn[1]) #our cube will move to this directions
                if i == len(self.body)-1: #if we are in the last cube we remove the turn
                    self.turns.pop(p)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtween = w // rows

    x=0
    y=0
    for i in range(rows):
        x = x+sizeBtween
        y= y+sizeBtween

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w)) #draw up,down lines across the screen
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))#draw side to side across the screen


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(r, item):
    positions = item.body  # Get all the posisitons of cubes in our snake

    while True:  # Keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            # This wll check if the position we generated is occupied by the snake
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, height, rows, s, snack
    width = height = 500
    rows = 20
    win = pygame.display.set_mode((width, height))
    s = snake ((255, 255, 255), (10,10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    running = True
    clock = pygame.time.Clock()
    while running:
        pygame.time.delay(50) #speed of the snake
        clock.tick(10) #speed of the snake
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)) :
            if s.body[x].pos in list(map(lambda x: x.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box("You lost", "Try Again")
                s.reset((10,10))
                break



        redrawWindow(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False





if __name__ == '__main__':
    main()