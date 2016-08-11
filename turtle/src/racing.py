import turtle
import random

wn = turtle.Screen()
wn.bgcolor("white")

homer = turtle.Turtle()
homer.speed(100)

marge = turtle.Turtle()
marge.speed(100)

#205 is the edge in any one given direction
#Max: 205, 205
#Min: -205, -205

edge = 205

homer.penup()
homer.setpos(50, 50)
marge.penup()
marge.setpos(-50, -50)
pos1 = (homer.position())
pos2 = (marge.position())

while pos1[0] < abs(edge) and pos2[0] < abs(edge):
    pos1 = (homer.position())
    pos2 = (marge.position())
    homer.forward(random.randint(0,10))
    marge.forward(random.randint(0,15))
    """
    if pos1 > pos2:
        print("Homer is winning! Woo hoo! \n")
    elif pos2 > pos1:
        print("Marge is winning! Aww yeah! \n")
    else:
        print("It's a dead heat! \n")
    """

if pos1 > pos2:
    print("Homer won! Woo hoo!")
elif pos2 > pos1:
    print("Marge won! Aww yeah!")
else:
    print("It's a tie!")