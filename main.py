import sys
import os
import ui
import commands
import data
from config import Color

# Pygame (Optional)
try:
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

os.system('') 
if os.name == 'nt':
    os.system('title ROOT_ACCESS_TERMINAL_v7.2')
    os.system('color 0A')

# ==========================================
# Game Engine
# ==========================================

class Game:
    def __init__(self):
        self.trace_rate = 0.0
        self.money = 500 # 초기 자금
        self.stage_idx = 0
        self.difficulty = "beginner"
        
        # Load Data
        self.local_vm, self.machines, self.stages_info = data.get_initial_data()
        self.current_vm = self.local_vm
        
        self.is_connected = False
        self.remote_user = "ghost"
        
        # 상태 플래그
        self.mail_read = False
        self.stage_email_opened = False # 현재 스테이지에서 이메일을 한 번이라도 열었는지
        self.stage_flags = {"killed_daemon": False, "wiped": False}
        
        self.init_audio()

    def init_audio(self):
        if not AUDIO_AVAILABLE: return
        try:
            pygame.mixer.init()
            if os.path.exists("bgm.mp3"):
                pygame.mixer.music.load("bgm.mp3")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            if os.path.exists("success.wav"):
                self.sfx_success = pygame.mixer.Sound("success.wav")
                self.sfx_success.set_volume(0.6)
            else: self.sfx_success = None
        except: pass

    def play_sfx(self, type="success"):
        if AUDIO_AVAILABLE and self.sfx_success and type == "success":
            self.sfx_success.play()
        elif type == "alert": print('\a')

    # --- UI & Visual Effects ---
    def draw_ui_box(self, content_lines, title=" SYSTEM ", color=Color.GREEN):
        ui.draw_ui_box(content_lines, title, color)

    def type_print(self, text, color=Color.GREEN, speed=0.03):
        ui.type_print(text, color, speed)

    def loading_bar(self, duration=1.0, message="Processing"):
        ui.loading_bar(duration, message)

    def show_logo(self):
        ui.show_logo()

    # --- Game Logic ---
    def select_difficulty(self):
        self.show_logo()
        self.draw_ui_box([
            "난이도를 선택하십시오:",
            f"[1] Beginner (요원) : J가 상세 명령어를 지시함",
            f"[2] Expert (베테랑) : 목표와 상황만 주어짐"
        ], title=" LOGIN REQUIRED ")
        
        while True:
            choice = input(">> ").strip()
            if choice == "1":
                self.difficulty = "beginner"
                break
            elif choice == "2":
                self.difficulty = "expert"
                break

    # --- Email System ---
    def draw_email(self):
        s = self.stages_info[self.stage_idx]
        body = s['beginner'] if self.difficulty == "beginner" else s['expert']

        # 최초 확인: 전체 UI 출력
        if not self.stage_email_opened:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Color.CYAN + "╔═══════════════════════════════════════════════════════════════╗")
            print(f"║ {Color.YELLOW}ENCRYPTED MESSAGE RECEIVED{Color.CYAN}".center(72))
            print("╠═══════════════════════════════════════════════════════════════╣")
            print(f"║ FROM: {s['email_sender']}".ljust(63) + "║")
            print(f"║ SUBJ: {s['email_sub']}".ljust(63) + "║")
            print("╚═══════════════════════════════════════════════════════════════╝" + Color.RESET)
            
            print("\n" + Color.WHITE + "Decrypting: ", end="")
            for _ in range(5):
                sys.stdout.write("█"); sys.stdout.flush(); ui.time.sleep(0.1)
            print(" [OK]" + Color.RESET + "\n")
            
            self.type_print(body, Color.WHITE, 0.02)
            print("\n" + Color.BLUE + "="*60 + Color.RESET)
            
            self.mail_read = True
            self.stage_email_opened = True # 읽음 처리
            input(f"\n{Color.GREEN}[Press Enter to Accept Mission]{Color.RESET}")
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_prompt_header()
        
        # 재확인: 인라인 텍스트 출력
        else:
            print(f"\n{Color.YELLOW}=== MISSION RECAP ==={Color.RESET}")
            print(f"{Color.CYAN}Target: {s['target']}{Color.RESET}")
            print(body)
            print(Color.YELLOW + "="*20 + Color.RESET)

    def print_prompt_header(self):
        s = self.stages_info[self.stage_idx]
        self.draw_ui_box([
            f"Target: {s['target']}",
            f"Trace: {self.trace_rate:.1f}% | Money: ${self.money}"
        ], title=" ACTIVE SESSION ")

    def update_trace(self, amount):
        self.trace_rate += amount
        if self.stage_idx == 4: self.trace_rate += 0.5 
        if self.trace_rate >= 100:
            self.play_sfx("alert")
            print(f"\n{Color.RED}!!! GAME OVER - ARRESTED !!!{Color.RESET}")
            sys.exit()

    def provide_hint(self):
        print(f"\n{Color.MAGENTA}[HINT] {self.stages_info[self.stage_idx]['beginner']}{Color.RESET}")

    # --- Command Parser ---
    def run_command(self, user_input):
        commands.execute_command(self, user_input)

    def check_mission(self, target, action):
        s = self.stages_info[self.stage_idx]
        done = False
        if action == "steal" and target == s['goal']: done = True
        elif action == "decrypt" and target == s['goal']: done = True
        elif action == "shred" and target == "wiper": done = True
        elif action == "webcam": done = True
        
        if done:
            self.complete_stage()

    def complete_stage(self):
        r = self.stages_info[self.stage_idx]['reward']
        news = self.stages_info[self.stage_idx]['news']
        self.money += r
        self.play_sfx("success")
        
        self.draw_ui_box([f"Mission Accomplished!", f"Reward: ${r}"], title=" SUCCESS ", color=Color.CYAN)
        print("\n" + Color.YELLOW + "[NEWS HEADLINE] " + news + Color.RESET)
            
        input("\nPress Enter...")
        self.stage_idx += 1; self.is_connected = False; self.current_vm = self.local_vm; self.trace_rate = 0
        self.mail_read = False; self.stage_email_opened = False # 메일 상태 초기화
        
        if self.stage_idx < len(self.stages_info): 
            print(f"\n{Color.YELLOW}New encrypted mail from J. Type 'email'.{Color.RESET}")
        else: print(f"\n{Color.GREEN}*** ALL CLEAR - J IS GONE ***{Color.RESET}"); sys.exit()

if __name__ == "__main__":
    g = Game()
    g.select_difficulty()
    print(f"\n{Color.YELLOW}You have an encrypted mail from J. Type 'email' to decrypt.{Color.RESET}")
    while True:
        try:
            prompt = f"\n{Color.RED if g.is_connected else Color.GREEN}┌──({g.remote_user}@{g.current_vm.ip})\n└─$ {Color.RESET}"
            cmd = input(prompt).strip()
            if cmd: g.run_command(cmd)
            if g.is_connected: g.update_trace(0.5)
        except KeyboardInterrupt:
            print("\nTerminated.")
            break
        except Exception as e:
            print(f"Error: {e}")