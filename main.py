import math

import MusicHandler
import argparse
import Dial
from tkinter import *

parser = argparse.ArgumentParser(description='Run the Radio Time Machine with the Path to the Music base folder.')
parser.add_argument('path', metavar="path", type=str, nargs=1,
                    help='The path to the music base')


def convert_angle_to_year(angle):
    angle *= -1
    angle += 180
    angle = angle / 1
    if angle - 90 < 0:
        angle += 270
    else:
        angle -= 90
    angle = (97 * angle / 360)
    return round(1920 + angle)


def convert_angle_to_month(angle):
    angle *= -1
    angle += 180
    angle = angle / 30
    if angle - 3 < 0:
        angle += 9
    else:
        angle -= 3
    return round(angle)


def on_dial_change_year(angle):
    year = convert_angle_to_year(angle)
    month = convert_angle_to_month(month_dial.angle)
    result = music.play_music(year, month)
    if result is not None:
        print("Changed Music to", result)
    else:
        print("No music for ",year,month)


def on_dial_change_month(angle):
    month = convert_angle_to_month(angle)
    year = convert_angle_to_year(year_dial.angle)
    result = music.play_music(year, month)
    if result is not None:
        print("Changed Music to", result)
    else:
        print("No music for ", year, month)


month_dial = None
year_dial = None
music = None

if __name__ == '__main__':
    master = Tk()
    master.title("Radio Time Machine")

    # Add a grid
    mainframe = Frame(master)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.pack(pady=0, padx=0)
    month_dial = Dial.Dial(mainframe, command=on_dial_change_month, radius='.75i', disp_type='month')
    current_step = 0
    steps = math.ceil((12 - 1) / 1)
    month_dial.canvas.grid(row=1, column=1)
    year_dial = Dial.Dial(mainframe, command=on_dial_change_year, radius='.75i', disp_type='year')
    year_dial.canvas.grid(row=1, column=2)

    args = parser.parse_args()
    music = MusicHandler.MusicHandler(args.path[0])

    master.mainloop()
