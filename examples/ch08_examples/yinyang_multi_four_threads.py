"""
yinyang_multi_four_threads.py

Code from "Python Programming Fundamentals" by Kent Lee
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


def draw_fish(heading, radius, color):
    pen = turtle.Turtle()
    pen.speed(10)
    pen.setheading(heading)
    pen.width(3)
    pen.color("black", color)  # pen color, fill color
    pen.begin_fill()
    pen.circle(radius/2., 180)
    pen.circle(radius, 180)
    pen.left(180)
    pen.circle(-radius/2., 180)
    pen.end_fill()


def draw_eye(heading, fish_radius, color):
    pen = turtle.Turtle()
    pen.speed(10)
    pen.setheading(heading)
    pen.left(90)
    pen.up()
    pen.forward(fish_radius*0.35)
    pen.right(90)
    pen.down()
    pen.color("black", color)
    pen.begin_fill()
    pen.circle(fish_radius*0.15)
    pen.end_fill()


def draw_yin_fish(radius):
    draw_fish(0, radius, "black")


def draw_yin_eye(fish_radius):
    draw_eye(0, fish_radius, "white")


def draw_yang_fish(radius):
    draw_fish(180, radius, "white")


def draw_yang_eye(fish_radius):
    draw_eye(180, fish_radius, "black")


def main():
    init_screen()

    fish_radius = 200

    threads = [
        Thread(target=draw_yin_fish, args=(fish_radius,)),
        Thread(target=draw_yin_eye, args=(fish_radius,)),
        Thread(target=draw_yang_fish, args=(fish_radius,)),
        Thread(target=draw_yang_eye, args=(fish_radius,)),
    ]

    for thread in threads:
        thread.start()

    turtle.mainloop()
    # main thread can't join child threads or turtle graphics complains


if __name__ == '__main__':
    main()
