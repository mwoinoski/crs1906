"""
yinyang_multithreaded.py

Code from "Python Programming Fundamentals" by Kent Lee

IMPORTANT: this application runs only with Python 3.11.
"""
import sys
import subprocess
from threading import Thread
import turtle  # turtle graphics library


# This program needs to run under Python 3.11
if f'{sys.version_info.major}.{sys.version_info.minor}' != '3.11':
    subprocess.run(['py', '-3.11', sys.argv[0]])
    exit()


def init_screen():
    """
    Delete the turtle's drawings from the screen, re-center the turtle and
    set variables to the default values
    """
    screen = turtle.Screen()
    screen.setup(width=500, height=500)
    screen.title('Yin Yang')

    turtle.reset()
    turtle.bgcolor('#E8E8F6')
    turtle.hideturtle()


def draw_fish(heading, radius, color1, color2):
    pen = turtle.Turtle()
    pen.speed(10)
    pen.setheading(heading)
    pen.width(3)
    pen.color("black", color1)  # pen color, fill color
    pen.begin_fill()
    pen.circle(radius/2., 180)
    pen.circle(radius, 180)
    pen.left(180)
    pen.circle(-radius/2., 180)
    pen.end_fill()

    # draw eye
    pen.left(90)
    pen.up()
    pen.forward(radius*0.35)
    pen.right(90)
    pen.down()
    pen.color(color1, color2)
    pen.begin_fill()
    pen.circle(radius*0.15)
    pen.end_fill()


def draw_yin():
    draw_fish(0, 200, "black", "white")


def draw_yang():
    draw_fish(180, 200, "white", "black")


def main():
    init_screen()

    yin_thread = Thread(target=draw_yin)
    yang_thread = Thread(target=draw_yang)

    yin_thread.start()
    yang_thread.start()

    turtle.mainloop()
    # main thread can't join child threads or turtle graphics complains

if __name__ == '__main__':
    main()
