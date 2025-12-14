import os

# Pygame Check
try:
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def init_system_settings():
    os.system('') 
    if os.name == 'nt':
        os.system('title ROOT_ACCESS_TERMINAL_v8.1_TUTORIAL_RESTORED')
        os.system('color 0A')