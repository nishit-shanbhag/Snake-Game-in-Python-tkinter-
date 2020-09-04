import tkinter as tk
from random import randrange as rd
from tkinter import font

from PIL import ImageTk, Image

WIDTH = 600
HEIGHT = 600
SCORE = 0
SPEED = 250
root = tk.Tk()

# extra 50 for top menu bar
w = tk.Canvas(root, width=WIDTH, height=HEIGHT + 50)

gameOver = False


def checkCollision():
    global gameOver

    temp = head.next
    while (temp is not None):
        if [head.x1, head.y1] == [temp.x1, temp.y1]:
            head.fill = "red"
            temp.fill = "red"
            gameOver = True

        temp = temp.next


class Box:
    def __init__(self, canvas=None, x1=-20, y1=-20, x2=0, y2=0, vX=20, vY=0, fill=None):
        self.canvas = canvas
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        # Velocity (direction)
        self.vX = vX
        self.vY = vY
        self.fill = fill

        # To access the object's rectange
        self.objId = None
        self.drawBox()
        self.next = None

    def drawBox(self):
        self.objId = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.fill)


    def __str__(self) -> str:
        if self.next is not None:
            return f"x1: {self.x1}, y1: {self.y1}, next: {str(self.next)}"
        else:
            return f"x1: {self.x1}, y1: {self.y1}, next: None"


apple_image = Image.open('apple.png')


def insertAtEnd(box):
    temp = head
    while temp.next is not None:
        temp = temp.next
    temp.next = box


def moveBox():
    print(str(head))

    temp = head
    prev_cords = [head.x1, head.y1, head.x2, head.y2]
    while (temp.next is not None):
        prev_cords[0], temp.next.x1 = temp.next.x1, prev_cords[0]
        prev_cords[1], temp.next.y1 = temp.next.y1, prev_cords[1]
        prev_cords[2], temp.next.x2 = temp.next.x2, prev_cords[2]
        prev_cords[3], temp.next.y2 = temp.next.y2, prev_cords[3]

        temp.next.canvas.coords(temp.next.objId, temp.next.x1, temp.next.y1, temp.next.x2, temp.next.y2)
        temp = temp.next

    head.x1 += head.vX
    head.x2 += head.vX
    head.y1 += head.vY
    head.y2 += head.vY
    head.canvas.coords(head.objId, head.x1, head.y1, head.x2, head.y2)
    checkCollision()


class Food:
    def __init__(self, canvas, x1, y1, x2, y2, fill):
        global apple_image
        self.canvas = canvas
        self.canvas.image = ImageTk.PhotoImage(apple_image)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.fill = fill
        self.objId = None
        self.drawFood()

    def drawFood(self):
        self.objId = self.canvas.create_image(self.x1 + 10, self.y1 + 10, image=w.image)
        # self.objId = self.canvas.create_oval(self.x1 + 1, self.y1 + 1, self.x2 - 1, self.y2 - 1, fill='black')

    # self.objId = self.canvas.create_rectangle(self.x1 + 1, self.y1 + 1, self.x2 - 1, self.y2 - 1, fill=self.fill,outline='black')
    def __del__(self):
        # self.canvas.coords(self.objId, -20, -20, 0, 0)
        pass


w.create_rectangle(0, 0, WIDTH, HEIGHT, fill='#9ac503')
# for i in range(0, WIDTH, 20):
#     w.create_line(i, 0, i, HEIGHT, fill='white')
#     w.create_line(0, i, WIDTH, i, fill='white')
w.pack()

head = Box(w, 20, 20, 40, 40, fill='black')


def keypress(e):
    global SPEED
    if e.char == 'a':
        if head.vX == 0:
            head.vX = -20
            head.vY = 0
        # box.moveBox(-20,0)
    elif e.char == 'd':
        if head.vX == 0:
            head.vX = 20
            head.vY = 0
        # box.moveBox(20,0)
    elif e.char == 'w':
        if head.vY == 0:
            head.vY = -20
            head.vX = 0
        # box.moveBox(0,-20)
    elif e.char == 's':
        if head.vY == 0:
            head.vY = 20
            head.vX = 0
    elif e.char == '0':
        # Refresh speed
        SPEED = int(SPEED / 2)
        # box.moveBox(0,20)
    elif e.char == "9":
        SPEED *= 2


root.bind('<Key>', keypress)

foodX = rd(0, WIDTH, 20)
foodY = rd(0, HEIGHT, 20)
isfoodPresent = True
f = Food(w, foodX, foodY, foodX + 20, foodY + 20, '#9ac503')
w.create_rectangle(0, 602, 600, 650, fill='black')
score_label = w.create_text(60, 630, text="SCORE: ", font=font.Font(family='Consolas', size=20, weight='bold'),
                            fill='#9ac503')
score_text = w.create_text(120, 630, text=SCORE, font=font.Font(family='Consolas', size=20, weight='bold'),
                           fill='#9ac503')

isRed = True


def blinkCollision():
    global isRed
    if isRed:
        head.objId = head.canvas.create_rectangle(head.x1, head.y1, head.x2, head.y2, fill="red")
    else:
        head.objId = head.canvas.create_rectangle(head.x1, head.y1, head.x2, head.y2, fill="black")
    isRed = not isRed




while True:
    if not gameOver:

        # Wait of speed (in ms) then refresh
        w.after(SPEED, moveBox())
        # If snake is in the corner
        if (head.x1 < 0):
            head.x1 = WIDTH
            head.x2 = WIDTH + 20
        elif (head.x1 > WIDTH - 20):
            head.x1 = 0
            head.x2 = 20
        if (head.y1 < 0):
            head.y1 = WIDTH
            head.y2 = WIDTH + 20
        elif (head.y1 > HEIGHT - 20):
            head.y1 = 0
            head.y2 = 20
        if not isfoodPresent:
            # Show apple at a random place
            foodX = rd(0, WIDTH, 20)
            foodY = rd(0, HEIGHT, 20)
            f = Food(w, foodX, foodY, foodX + 20, foodY + 20, '#9ac503')
            isfoodPresent = True
        if head.x1 == f.x1 and head.y1 == f.y1:
            SCORE += 1

            temp = head
            head = Box(w, f.x1, f.y1, f.x2, f.y2, head.vX, head.vY, 'black')
            head.next = temp

            print("Copied\nhead: ", head.x1, ",", head.y1, "\ttemp: ", temp.x1, ", ", temp.y1)
            w.delete(score_text)
            score_text = w.create_text(120, 630, text=SCORE, font=font.Font(family='Consolas', size=20, weight='bold'),
                                       fill='#9ac503')

            # Increase speed to twice after every 5 score
            if SCORE % 5 == 0 and SCORE >= 5 and SCORE < 30:
                SPEED = int(SPEED / 2)
            print(SPEED)
            isfoodPresent = False
            w.delete(f)
    else:
        gameOver_box1 = w.create_rectangle(HEIGHT / 2 - 105, HEIGHT / 2 - 55, HEIGHT / 2 + 105, HEIGHT / 2 + 55,
                                           fill='black')
        gameOver_box2 = w.create_rectangle(HEIGHT / 2 - 100, HEIGHT / 2 - 50, HEIGHT / 2 + 100, HEIGHT / 2 + 50,
                                           fill='#9ac503')
        temp = head
        while(temp is not None):
            temp.canvas.create_rectangle(temp.x1, temp.y1, temp.x2, temp.y2, fill="black")
            temp = temp.next

        w.after(1000, blinkCollision())
        gameOver_text = w.create_text(HEIGHT / 2, HEIGHT / 2, text='GAME OVER',
                                      font=font.Font(family='Consolas', size=20, weight='bold'), fill='black')

    root.update()
