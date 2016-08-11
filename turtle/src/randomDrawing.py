import turtle
import random

wn = turtle.Screen()
wn.bgcolor("white")

bob = turtle.Turtle()
bob.speed(100)
times = 100
color = 0

for i in range(times):
    facing = random.randint(1,3)
    turn = random.randint(0,360)
    colors = []
    for i in range(0, 3):
        color = random.randint(10,256)
        colors.append(color)
    bob.pencolor(colors)
    if facing == 1:
        bob.left(turn)
    else:
        bob.right(turn)
    bob.forward(random.randint(0,20))