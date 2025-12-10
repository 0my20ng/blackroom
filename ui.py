import sys
import time
import os
from config import Color

def draw_ui_box(content_lines, title=" SYSTEM ", color=Color.GREEN):
    width = 65
    print(color + "╔" + "═" * (width - 2) + "╗")
    print(f"║{title.center(width - 2)}║")
    print("╠" + "═" * (width - 2) + "╣")
    for line in content_lines:
        while len(line) > width - 4:
            print(f"║ {line[:width-4]} ║")
            line = line[width-4:]
        print(f"║ {line.ljust(width - 4)} ║")
    print("╚" + "═" * (width - 2) + "╝" + Color.RESET)

def type_print(text, color=Color.GREEN, speed=0.03):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(Color.RESET + "\n")

def loading_bar(duration=1.0, message="Processing"):
    print(f"{message}...", end="", flush=True)
    width = 20
    sys.stdout.write(f" [{'-'*width}]")
    sys.stdout.flush()
    sys.stdout.write("\b" * (width+1))
    for i in range(width):
        time.sleep(duration / width)
        sys.stdout.write("#")
        sys.stdout.flush()
    sys.stdout.write("] Done.\n")

def show_logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Color.GREEN + r"""
  _____             _        _                          
 |  __ \           | |      | |                         
 | |__) |___   ___ | |_     | |     ___  ___ ___  ___  
 |  _  // _ \ / _ \| __|    | |    / __|/ __/ _ \/ __| 
 | | \ \ (_) | (_) | |_     | |____\__ \ (_|  __/\__ \ 
 |_|  \_\___/ \___/ \__|    |______|___/\___\___||___/ 
                                           v7.2
        """ + Color.RESET)
    print(f"{Color.CYAN}       Connection Established... Difficulty Selection.{Color.RESET}\n")
