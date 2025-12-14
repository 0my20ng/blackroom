import sys
import time
import os
from config import Color, init_system_settings
from models import VirtualMachine
from ui import draw_ui_box, type_print, show_logo, init_audio, play_sfx
import data
from commands import process_command as run_command_logic

class Game:
    def __init__(self):
        self.trace_rate = 0.0
        self.money = 500
        self.stage_idx = 0
        self.difficulty = "beginner"
        self.local_vm = VirtualMachine("Localhost", "127.0.0.1", 
                                       files=data.get_init_local_files())
        self.current_vm = self.local_vm
        self.is_connected = False
        self.remote_user = "ghost"
        self.mail_read = False
        self.stage_email_opened = False
        
        self.sfx_success = init_audio()
        self.machines = data.setup_machines()
        self.stages_info = data.get_stages_info()
        self.stage_flags = {"killed_watchdog": False, "killed_locker": False, "framed_ip": False}

    def play_sfx(self, type="success"):
        play_sfx(self.sfx_success, type)

    def draw_ui_box(self, content_lines, title=" SYSTEM ", color=Color.GREEN):
        draw_ui_box(content_lines, title, color)

    def draw_email(self):
        s = self.stages_info[self.stage_idx]
        body = s['beginner'] if self.difficulty == "beginner" else s['expert']
        
        # 최초 확인 시: 전체 화면 전환
        if not self.stage_email_opened:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Color.CYAN + "╔═══════════════════════════════════════════════════════════════╗")
            print(f"║ {Color.YELLOW}ENCRYPTED MESSAGE RECEIVED{Color.CYAN}".center(72))
            print("╠═══════════════════════════════════════════════════════════════╣")
            print(f"║ FROM: {s.get('email_sender', 'UNKNOWN')}".ljust(63) + "║")
            print(f"║ SUBJ: {s.get('email_sub', 'NO SUBJECT')}".ljust(63) + "║")
            print("╚═══════════════════════════════════════════════════════════════╝" + Color.RESET)
            print("\n" + Color.WHITE + "Decrypting: ", end=""); time.sleep(0.5); print("[OK]" + Color.RESET + "\n")
            type_print(body, Color.WHITE, 0.02)
            self.mail_read = True
            self.stage_email_opened = True
            input(f"\n{Color.GREEN}[Press Enter]{Color.RESET}")
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_prompt_header()
        
        # 재확인 시: 인라인 텍스트 출력
        else:
            print(f"\n{Color.YELLOW}=== MISSION RECAP ==={Color.RESET}")
            print(f"{Color.CYAN}Target: {s.get('target', 'UNKNOWN')}{Color.RESET}")
            print(body)
            print(Color.YELLOW + "="*20 + Color.RESET)

    def print_prompt_header(self):
        s = self.stages_info[self.stage_idx]
        self.draw_ui_box([
            f"Target: {s.get('target', 'UNKNOWN')}",
            f"Trace: {self.trace_rate:.1f}% | Money: ${self.money}"
        ], title=" ACTIVE SESSION ")

    def update_trace(self, amount):
        self.trace_rate += amount
        if self.stage_idx == 4: self.trace_rate += 0.5 
        if self.trace_rate >= 100:
            self.play_sfx("alert")
            print(f"\n{Color.RED}!!! SYSTEM LOCKDOWN - CAUGHT !!!{Color.RESET}")
            sys.exit()

    def run_command(self, user_input):
        run_command_logic(self, user_input)

    def check_mission(self, target, action):
        s = self.stages_info[self.stage_idx]
        done = False
        if action == "steal" and target == s.get('goal'): done = True
        elif action == "decrypt" and target == s.get('goal'): done = True
        elif action == "shred" and target == s.get('goal'): done = True
        elif action == "webcam": done = True
        
        if done:
            self.complete_stage()

    def complete_stage(self):
        r = self.stages_info[self.stage_idx].get('reward', 0)
        news = self.stages_info[self.stage_idx].get('news', '')
        self.money += r
        self.play_sfx("success")
        
        self.draw_ui_box([f"Mission Accomplished!", f"Reward: ${r}"], title=" SUCCESS ", color=Color.CYAN)
        if news:
            print("\n" + Color.YELLOW + "[NEWS] " + news + Color.RESET)
            
        input("\nPress Enter...")
        self.stage_idx += 1; self.is_connected = False; self.current_vm = self.local_vm; self.trace_rate = 0
        self.mail_read = False; self.stage_email_opened = False
        
        if self.stage_idx < len(self.stages_info): 
            print(f"\n{Color.YELLOW}New mail from J. Type 'email'.{Color.RESET}")
        else: print(f"\n{Color.GREEN}*** ALL CLEAR ***{Color.RESET}"); sys.exit()

    def select_difficulty(self):
        show_logo()
        self.draw_ui_box([
            "난이도를 선택하십시오:",
            "[1] Beginner (요원) : J가 상세 명령어를 지시함",
            "[2] Expert (베테랑) : 목표와 상황만 주어짐"
        ], title=" LOGIN REQUIRED ")
        
        while True:
            c = input(">> ").strip()
            if c == "1": self.difficulty = "beginner"; break
            elif c == "2": self.difficulty = "expert"; break

if __name__ == "__main__":
    init_system_settings()
    g = Game()
    g.select_difficulty()
    print(f"\n{Color.YELLOW}New mail from J. Type 'email'.{Color.RESET}")
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
            pass