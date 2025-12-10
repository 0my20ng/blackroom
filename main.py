import sys
import time
import os
import random

# Pygame (Optional)
try:
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# ==========================================
# 1. 설정 및 데이터 (Config)
# ==========================================

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

os.system('') 

if os.name == 'nt':
    os.system('title ROOT_ACCESS_TERMINAL_v7.2')
    os.system('color 0A')

MANUAL = {
    "nmap": "사용법: nmap [IP]\n설명: [정찰] 타겟 서버를 스캔하여 **열려있는 포트 번호**를 찾아냅니다. (가장 먼저 해야 할 일)",
    "analyze": "사용법: analyze [IP] [Port]\n설명: [분석] nmap으로 찾은 포트의 상세 서비스 버전을 확인합니다.",
    "searchsploit": "사용법: searchsploit [서비스명]\n설명: [분석] 해당 서비스의 알려진 공격 방법(Exploit)을 찾습니다.",
    "ssh": "사용법: ssh [ID]@[IP]\n설명: [접속] 아이디와 비밀번호로 서버에 접속합니다.",
    "ftp": "사용법: ftp [IP]\n설명: [접속] 파일 전송 서버입니다. 익명(anonymous) 접속이 가능한지 확인하세요.",
    "hydra": "사용법: hydra -l [ID] [IP]\n설명: [공격] SSH 비밀번호를 무차별 대입하여 뚫습니다. ID를 먼저 알아내야 합니다.",
    "hashcat": "사용법: hashcat [해시값]\n설명: [해독] 암호화된 해시 문자열을 평문 비밀번호로 복구합니다.",
    "web_scan": "사용법: web_scan [IP]\n설명: [공격] 웹 서버에 숨겨진 관리자 페이지나 파일을 크롤링합니다.",
    "metasploit": "사용법: metasploit\n설명: [공격] 방화벽을 우회하고 시스템 권한을 강제로 탈취합니다.",
    "ls": "파일 목록 보기", "cat": "파일 읽기",
    "scp": "파일 다운로드 (목표 달성용)", "decrypt": "파일 암호 해독",
    "shred": "파일 영구 삭제", "edit_log": "로그 조작 (추적 방지)",
    "ps": "프로세스 확인", "kill": "프로세스 종료",
    "chmod": "권한 변경 (+x)", "run": "스크립트 실행 (./)",
    "email": "이메일 확인", "hint": "힌트 보기"
}

# ==========================================
# 2. 시스템 클래스 (System)
# ==========================================

class VirtualMachine:
    def __init__(self, name, ip, files=None, users=None, ports=None, services=None, processes=None):
        self.name = name
        self.ip = ip
        self.cwd = "/" 
        self.users = users if users else {} 
        self.ports = ports if ports else []
        self.services = services if services else {}
        self.processes = processes if processes else {}
        self.files = files if files else {"/": {}}
        self.dirs = {"/": []}
        
        for path in self.files:
            if path not in self.dirs: self.dirs[path] = []
            
    def list_files(self):
        files = list(self.files.get(self.cwd, {}).keys())
        dirs = self.dirs.get(self.cwd, [])
        return files, dirs

    def get_file_content(self, filename):
        current_files = self.files.get(self.cwd, {})
        for f in current_files:
            if f.lower() == filename.lower():
                return current_files[f]
        return None

    def change_dir(self, target):
        if target == "..":
            if self.cwd == "/": return False
            self.cwd = "/".join(self.cwd.split("/")[:-1])
            if self.cwd == "": self.cwd = "/"
            return True
        if target.startswith("/"): new_path = target
        else: new_path = (self.cwd + "/" + target) if self.cwd != "/" else "/" + target
        if new_path in self.files or new_path in self.dirs:
            self.cwd = new_path
            return True
        return False

# ==========================================
# 3. 게임 엔진 (Game Engine)
# ==========================================

class Game:
    def __init__(self):
        self.trace_rate = 0.0
        self.money = 500 # 초기 자금
        self.stage_idx = 0
        self.difficulty = "beginner"
        self.local_vm = VirtualMachine("Localhost", "127.0.0.1", 
                                       files={"/": {"manual.txt": "Type 'man' to read", "contract_j.txt": "J takes 70%, You take 30%."}})
        self.current_vm = self.local_vm
        self.is_connected = False
        self.remote_user = "ghost"
        
        # 상태 플래그
        self.mail_read = False
        self.stage_email_opened = False # 현재 스테이지에서 이메일을 한 번이라도 열었는지
        
        self.init_audio()
        self.setup_data()

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

    def setup_data(self):
        # 1. Tutorial VM
        vm_tut = VirtualMachine("Test_Server", "10.0.0.1", 
                                files={"/": {"hello.txt": "Welcome agent.", "payment_log.txt": "Target: Ghost | Status: Underpaid"}},
                                users={"guest": "1234"},
                                ports=["22/tcp"], services={"22": "OpenSSH (Weak Password)"})
        
        # 2. Stage 1 VM (BioTech)
        vm_bio = VirtualMachine("BioTech", "192.168.10.5",
                                files={
                                    "/": {"staff_hash.txt": "dr_mario:5f4dcc3b5aa765d61d8327deb882cf99"}, 
                                    "/home/dr_mario": {
                                        "formula_x.pdf": "DATA", 
                                        "memo.txt": "J asked for a backdoor... I refused."
                                    }
                                },
                                users={"dr_mario": "password"},
                                ports=["21/tcp", "22/tcp"], services={"21": "vsftpd (Anonymous Login Allowed)", "22": "OpenSSH"})
        vm_bio.dirs["/"] = ["home"]; vm_bio.dirs["/home"] = ["dr_mario"]; vm_bio.files["/home"] = {}

        # 3. Stage 2 VM (Ransom)
        vm_ran = VirtualMachine("Ransom_C2", "45.33.22.11",
                                files={"/var/www/hidden": {
                                    "master_key.txt": "key: money_is_king",
                                    "patient_data.enc": "[ENCRYPTED]",
                                    "chat_log.txt": "Broker_J: I want 50% of the ransom. Or I leak your IP."
                                }},
                                users={}, ports=["80/tcp"], services={"80": "Apache (Vuln: Dir Traversal)"},
                                processes={104: "httpd", 882: "ransom_daemon"})
        
        # 4. Stage 3 VM (CyberCloud)
        vm_cloud = VirtualMachine("CyberCloud", "10.20.30.40",
                                  files={
                                      "/var/www": {"config.php": "db_user:admin"},
                                      "/home/admin": {"source_code.zip": "Code", "wiper.sh": "#!/bin/bash\nrm -rf /"}
                                  },
                                  users={"admin": "dragon123"},
                                  ports=["80/tcp", "22/tcp"], services={"80": "nginx (Vuln: SQL Injection)", "22": "OpenSSH"})
        vm_cloud.dirs["/"] = ["var", "home"]; vm_cloud.dirs["/var"] = ["www"]; vm_cloud.dirs["/home"] = ["admin"]

        # 5. Stage 4 VM (Apex)
        vm_apex = VirtualMachine("Apex_Main", "172.16.99.99",
                                 files={"/root/secret": {"ledger.xlsx": "Corruption Proof", "cam.exe": "Running"}},
                                 users={"root": "0day"},
                                 ports=["Firewall"], services={"Firewall": "Stateful Inspection"})

        self.machines = {"10.0.0.1": vm_tut, "192.168.10.5": vm_bio, "45.33.22.11": vm_ran, "10.20.30.40": vm_cloud, "172.16.99.99": vm_apex}

        # 시나리오 데이터
        self.stages_info = [
            {
                "target": "10.0.0.1", "goal": "hello.txt", "reward": 500, "name": "Tutorial",
                "email_sub": "계약 시작: 접속 테스트",
                "email_sender": "J (Broker)",
                "beginner": """GHOST, 자네 실력을 봐야겠어. IP는 [10.0.0.1] 이다.
1. 'nmap 10.0.0.1'을 입력해 **포트 번호**를 찾아내.
2. 찾은 포트(22번)를 'analyze 10.0.0.1 22'로 분석해.
3. 'ssh guest@10.0.0.1' (비번: 1234)로 접속해.
4. 'scp hello.txt' 로 파일을 가져오면 합격이다.""",
                "expert": """GHOST, 자네 이름값은 들었어. 
내 개인 테스트 서버(10.0.0.1)에 'hello.txt' 파일을 놔뒀어.
가져오게. 방법은 묻지 마. 포트 스캔부터 시작하게.""",
                "news": ">> [속보] 다크웹 신규 해커 그룹 'GHOST', 활동 개시..."
            },
            {
                "target": "192.168.10.5", "goal": "formula_x.pdf", "reward": 2000, "name": "BioTech Theft",
                "email_sub": "의뢰: B사 신약 데이터",
                "email_sender": "J (Broker)",
                "beginner": """돈 냄새가 나는 건이야. B사(192.168.10.5)다.
1. 'nmap 192.168.10.5'로 포트를 확인해. (21번이 보일거야)
2. 'analyze 192.168.10.5 21'로 분석하면 'Anonymous' 접속 가능 여부가 나온다.
3. 'ftp 192.168.10.5'로 접속해서 파일을 뒤져.
4. 해시 파일이 나오면 다운받고 'hashcat'으로 비번을 뚫어.
5. 알아낸 비번으로 SSH 접속 후 'scp formula_x.pdf'.""",
                "expert": """B사(192.168.10.5) 녀석들이 불법 임상실험 데이터를 가지고 있어.
경쟁사가 그 데이터(formula_x.pdf)를 원해. 
FTP 포트 관리가 허술하다는 소문이 있어. 
직접 들어가진 못하더라도, 직원 ID나 암호화된 비밀번호 정도는 건질 수 있을 거야.
해독(hashcat)은 알아서 하게.""",
                "news": ">> [경제] B제약, 핵심 기술 유출 의혹에 주가 14% 급락."
            },
            {
                "target": "45.33.22.11", "goal": "patient_data.enc", "reward": 3000, "name": "Ransom Decrypt",
                "email_sub": "긴급: 병원 랜섬웨어 건",
                "email_sender": "J (Broker)",
                "beginner": """병원장이 뒷돈을 찔러줬어. C2 서버 IP는 45.33.22.11 야.
1. 'nmap 45.33.22.11'로 확인. 80번(웹)이 열려있을 거야.
2. 'web_scan 45.33.22.11'로 숨겨진 키 파일을 찾아.
3. 접속되면 'ps'로 악성 프로세스(PID: 882)를 확인해.
4. 'kill 882'로 놈을 멈추고 'decrypt patient_data.enc [키]'.""",
                "expert": """종합병원 서버가 랜섬웨어에 잠겼어. 
범인들 서버 IP는 45.33.22.11 야. 웹 서버 기반이지.
숨겨진 키 파일을 찾아서 데이터를 복구(decrypt)해.
아, 그리고 놈들이 백그라운드에 감시 프로그램을 돌리고 있을 테니, 
확실하게 프로세스부터 죽이고 작업해. 실수해서 돈 날리지 말고.""",
                "news": ">> [사회] 종합병원 전산망 마비 사태, 익명의 전문가 도움으로 극적 복구."
            },
            {
                "target": "10.20.30.40", "goal": "source_code.zip", "reward": 5000, "name": "Cyber Sabotage",
                "email_sub": "파괴 공작: C사 프로젝트",
                "email_sender": "J (Broker)",
                "beginner": """C사(10.20.30.40)를 파괴해라.
1. 'nmap' 확인 후 'searchsploit nginx'로 취약점 검색.
2. 정보로 'ssh admin@10.20.30.40' (PW: dragon123) 접속.
3. 'ls' 해보면 'wiper.sh'가 있지만 실행 권한이 없어.
4. 'chmod +x wiper.sh'로 권한 부여.
5. 중요: 'edit_log' 먼저 하고 './wiper.sh' 실행.""",
                "expert": """C사(10.20.30.40)가 우리 클라이언트의 아이디어를 베꼈어.
그냥 두면 내 클라이언트가 망해. 그럼 내 수수료도 날아가지.
DB를 털어서라도 관리자 권한을 얻어내.
그리고 소스코드를 완전히 갈아버려(shred).
가장 중요한 건, 경쟁사 IP로 로그를 조작(edit_log)해서 우릴 추적 못 하게 하는 거야.""",
                "news": ">> [IT] 게임사 C, 신작 소스코드 전량 소실... 내부 소행 가능성 제기."
            },
            {
                "target": "172.16.99.99", "goal": "ledger.xlsx", "reward": 0, "name": "The Betrayal",
                "email_sub": "경고: 당신은 발각되었습니다",
                "email_sender": "UNKNOWN",
                "beginner": """J가 배신했다! 172.16.99.99!
1. 'nmap -Pn 172.16.99.99' (방화벽 우회).
2. 'metasploit' (강제 침투).
3. 'webcam_snap' (증거 확보).""",
                "expert": """[SENDER: UNKNOWN]
도망쳐! J가 FBI에 당신의 위치 정보를 넘겼습니다.
모든 죄를 당신에게 뒤집어씌우고 잠적할 계획입니다.
J는 지금 방화벽으로 보호된 안전 가옥 서버(172.16.99.99)에 숨어있습니다.
살고 싶다면, 놈의 시스템을 강제로 뚫고(metasploit)
비리 장부와 놈의 얼굴 사진(webcam)을 확보해 FBI에 넘기세요.""",
                "news": ">> [속보] 국제 사이버 브로커 'J', 자택에서 FBI에 체포. 공범의 제보 결정적."
            }
        ]
        self.stage_flags = {"killed_daemon": False, "wiped": False}

    # --- UI & Visual Effects ---
    def draw_ui_box(self, content_lines, title=" SYSTEM ", color=Color.GREEN):
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

    def type_print(self, text, color=Color.GREEN, speed=0.03):
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        sys.stdout.write(Color.RESET + "\n")

    def loading_bar(self, duration=1.0, message="Processing"):
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

    def show_logo(self):
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

    # --- Email System (Updated) ---
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
                sys.stdout.write("█"); sys.stdout.flush(); time.sleep(0.1)
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
        parts = user_input.split()
        if not parts: return
        cmd = parts[0].lower()
        arg1 = parts[1] if len(parts) > 1 else None
        arg2 = parts[2] if len(parts) > 2 else None
        arg3 = parts[3] if len(parts) > 3 else None
        
        target = self.stages_info[self.stage_idx]['target']

        # 메일 안 읽었으면 차단
        if not self.mail_read and cmd != "email" and cmd != "exit":
            print(f"{Color.YELLOW}You have unread mail from J. Type 'email'.{Color.RESET}")
            return

        if cmd == "email": self.draw_email(); return
        if cmd == "exit":
            if self.is_connected: self.is_connected = False; self.current_vm = self.local_vm; self.remote_user = "ghost"; print("Disconnected.")
            else: sys.exit()
            return
        elif cmd == "help": print(f"{Color.CYAN}Commands: email, nmap, analyze, ssh, ftp, hydra, hashcat, web_scan, searchsploit, sqlmap, metasploit, ps, kill, chmod, ./run, ls, cat, scp, decrypt, shred, edit_log{Color.RESET}"); return
        elif cmd == "man": 
            if arg1 and arg1 in MANUAL: print(f"{Color.BLUE}{MANUAL[arg1]}{Color.RESET}")
            else: print("Usage: man [command]")
            return
        elif cmd == "status": 
             self.draw_ui_box([f"Trace: {self.trace_rate:.1f}%", f"Money: ${self.money}"], title=" STATUS ")
             return
        elif cmd == "hint": self.provide_hint(); return

        # Local Commands
        if not self.is_connected:
            if cmd == "nmap":
                self.update_trace(2)
                if arg1 == target or (self.stage_idx == 4 and arg1 == "-Pn"):
                    self.loading_bar(1.0, "Scanning")
                    if target in self.machines:
                        for p in self.machines[target].ports: print(f"{Color.GREEN}[+] {p} open{Color.RESET}")
                    else: print("Error: IP not found.")
                else: print("Target unreachable.")

            elif cmd == "analyze":
                self.update_trace(2)
                if arg1 == target and arg2:
                    self.loading_bar(0.8, "Analyzing")
                    print(f"{Color.GREEN}>> {self.machines[target].services.get(arg2, 'Unknown')}{Color.RESET}")
                else: print("Usage: analyze [IP] [Port]")

            elif cmd == "searchsploit":
                if self.stage_idx == 3 and arg1 and "nginx" in arg1.lower():
                    print(f"{Color.GREEN}[+] Exploit Found! Creds: ssh admin@10.20.30.40 (pw: dragon123){Color.RESET}")
                else: print("No exploit found.")

            elif cmd == "hashcat":
                self.update_trace(3)
                if self.stage_idx == 1 and arg1 == "5f4dcc3b5aa765d61d8327deb882cf99":
                    self.loading_bar(2.0, "Cracking")
                    print(f"{Color.GREEN}[CRACKED] password{Color.RESET}")
                else: print("Hash invalid or failed.")

            elif cmd == "ftp":
                if arg1 == target and self.stage_idx == 1:
                    print("Anonymous Login OK."); self.local_vm.files["/"]["staff_hash.txt"] = "dr_mario:5f4dcc3b5aa765d61d8327deb882cf99"
                    print(">> Downloaded.")
                else: print("Refused.")

            elif cmd == "hydra":
                self.update_trace(5)
                if arg1 == "-l" and arg3:
                    target_vm = self.machines.get(arg3)
                    if target_vm:
                        self.loading_bar(1.5, "Brute-forcing")
                        found = False
                        for u, pw in target_vm.users.items():
                            if u.lower() == arg2.lower():
                                print(f"{Color.GREEN}[SUCCESS] PW: {pw}{Color.RESET}")
                                found = True; break
                        if not found: print("Failed.")
                    else: print("Bad IP.")
                else: print("Usage: hydra -l [ID] [IP]")

            elif cmd == "web_scan":
                if arg1 == target and self.stage_idx == 2:
                    self.loading_bar(1.5, "Scanning")
                    print(f"{Color.GREEN}[+] Key Found.{Color.RESET}"); self.is_connected = True; self.current_vm = self.machines[target]; self.remote_user="www-data"; self.current_vm.cwd="/var/www/hidden"
                else: print("Nothing.")

            elif cmd == "sqlmap":
                print("Use 'searchsploit' instead.")

            elif cmd == "metasploit":
                if self.stage_idx == 4:
                    self.loading_bar(2.0, "Zero-Day Attack")
                    print(f"{Color.GREEN}>> ROOT ACCESS{Color.RESET}")
                    self.is_connected = True; self.current_vm = self.machines[target]; self.remote_user="root"; self.current_vm.cwd="/root/secret"
                else: print("Not needed.")

            elif cmd == "ssh":
                if arg1 and "@" in arg1:
                    u, i = arg1.split("@")
                    if i in self.machines:
                        pw = input("Password: ")
                        if (i == "192.168.10.5" and pw == "password") or \
                           (i == "10.20.30.40" and pw == "dragon123") or \
                           (i == "10.0.0.1" and pw == "1234"):
                            self.is_connected = True; self.current_vm = self.machines[i]; self.remote_user = u; print("Logged In.")
                            if u == "dr_mario": self.current_vm.cwd = "/home/dr_mario"
                            elif u == "admin": self.current_vm.cwd = "/home/admin"
                        else: print("Login Failed."); self.update_trace(5)
                    else: print("Unknown Host.")
                else: print("Usage: ssh [user]@[IP]")
            
            elif cmd in ["ls", "cat"]: self.sys_cmd(cmd, arg1)
            else: print("Error.")

        else: # Remote
            if cmd in ["ls", "cd", "cat"]: self.sys_cmd(cmd, arg1)
            elif cmd == "ps":
                print("PID\tPROCESS")
                for pid, name in self.current_vm.processes.items(): print(f"{pid}\t{name}")
            elif cmd == "kill":
                if self.stage_idx == 2 and arg1 == "882":
                    print("Killed."); self.stage_flags['killed_daemon'] = True
                else: print("Bad PID.")
            elif cmd == "chmod":
                if arg1 == "+x" and arg2 == "wiper.sh": print("Permission Granted.")
                else: print("Usage: chmod +x [file]")
            elif cmd == "./wiper.sh":
                if self.stage_idx == 3:
                    print("Wiping..."); self.stage_flags['wiped'] = True; self.check_mission("wiper", "shred")
                else: print("Denied.")
            
            elif cmd == "scp":
                if self.current_vm.get_file_content(arg1): print("Downloaded."); self.check_mission(arg1, "steal")
                else: print("File not found.")
            elif cmd == "decrypt":
                if self.stage_idx == 2:
                    if self.stage_flags['killed_daemon']: print("Decrypted."); self.check_mission("patient_data.enc", "decrypt")
                    else: print(f"{Color.RED}[ERROR] Daemon active!{Color.RESET}"); self.update_trace(10)
                else: print("Error.")
            elif cmd == "edit_log":
                self.loading_bar(1.0, "Modifying Logs")
                print(">> Logs Framed.")
            elif cmd == "shred":
                if self.stage_idx == 3:
                    print("Warning: Use the wiper script."); 
                else: print("Shredding...")
            elif cmd == "webcam_snap":
                if self.stage_idx == 4: print(">> Captured."); self.check_mission("j.jpg", "webcam")
            else: print("Error.")

    def sys_cmd(self, cmd, arg):
        vm = self.current_vm
        if cmd == "ls":
            f, d = vm.list_files()
            print("  ".join([f"{Color.BLUE}{x}/{Color.RESET}" for x in d] + f))
        elif cmd == "cd": vm.change_dir(arg)
        elif cmd == "cat":
            c = vm.get_file_content(arg)
            if c:
                color = Color.MAGENTA if "J" in c or "Broker" in c else Color.WHITE
                print(color + f"--- {arg} ---\n{c}" + Color.RESET)
            else: print("File not found")

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