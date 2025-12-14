import sys
import time
import os
from config import Color, AUDIO_AVAILABLE

# Try importing pygame for type hinting mostly, actual check is via AUDIO_AVAILABLE
try:
    import pygame
except ImportError:
    pass

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
                                           v8.0
    """ + Color.RESET)
    print(f"{Color.CYAN}       Connection Established... Target Acquired.{Color.RESET}\n")

def init_audio():
    sfx_success = None
    if not AUDIO_AVAILABLE: 
        return None
    try:
        pygame.mixer.init()
        if os.path.exists("bgm.mp3"):
            pygame.mixer.music.load("bgm.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        if os.path.exists("success.wav"):
            sfx_success = pygame.mixer.Sound("success.wav")
            sfx_success.set_volume(0.6)
    except: 
        pass
    return sfx_success

def play_sfx(sfx_success, type="success"):
    if AUDIO_AVAILABLE and sfx_success and type == "success":
        sfx_success.play()
    elif type == "alert": 
        print('\a')
