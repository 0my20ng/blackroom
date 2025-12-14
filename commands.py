import sys
import time
from config import Color
from ui import loading_bar
from data import MANUAL

def process_command(game, user_input):
    parts = user_input.split()
    if not parts: return
    cmd = parts[0].lower()
    arg1 = parts[1] if len(parts) > 1 else None
    arg2 = parts[2] if len(parts) > 2 else None
    arg3 = parts[3] if len(parts) > 3 else None
    
    s = game.stages_info[game.stage_idx]
    target = s['target']

    if not game.mail_read and cmd != "email" and cmd != "exit":
        print(f"{Color.YELLOW}Check email first.{Color.RESET}"); return

    if cmd == "email": game.draw_email(); return
    if cmd == "exit":
        if game.is_connected: game.is_connected = False; game.current_vm = game.local_vm; game.remote_user = "ghost"; print("Disconnected.")
        else: sys.exit()
        return
    elif cmd == "help": print(f"{Color.CYAN}Commands: nmap, web_scan, analyze, searchsploit, ssh, ftp, hydra, hashcat, metasploit, ls, cat, cd, ps, kill, chmod, run(./), grep, scp, decrypt, shred, edit_log{Color.RESET}"); return
    elif cmd == "man": 
        if arg1 and arg1 in MANUAL: print(f"{Color.BLUE}{MANUAL[arg1]}{Color.RESET}")
        else: print("Usage: man [command]")
        return
    elif cmd == "hint": print(f"\n{Color.MAGENTA}[HINT] {s['beginner']}{Color.RESET}"); return
    elif cmd == "status": 
            game.draw_ui_box([f"Trace: {game.trace_rate:.1f}%", f"Money: ${game.money}"], title=" STATUS ")
            return

    # Local
    if not game.is_connected:
        if cmd == "nmap":
            game.update_trace(2)
            if arg1 == target or (game.stage_idx == 4 and arg1 == "-Pn"):
                loading_bar(1.0, "Scanning")
                if target in game.machines:
                    for p in game.machines[target].ports: print(f"{Color.GREEN}[+] {p} open{Color.RESET}")
                else: print("Error.")

        elif cmd == "analyze":
            if arg1 == target and arg2:
                loading_bar(0.8, "Analyzing")
                print(f"{Color.GREEN}>> {game.machines[target].services.get(arg2, 'Unknown')}{Color.RESET}")
            else: print("Usage: analyze [IP] [Port]")

        elif cmd == "web_scan":
            if game.stage_idx == 1 and arg1 == target:
                loading_bar(1.0); print(f"{Color.GREEN}[+] Employee ID Found: dr_mario{Color.RESET}")
            elif game.stage_idx == 2 and arg1 == target:
                loading_bar(1.0); print(f"{Color.GREEN}[+] Key Found. Auto-Connecting...{Color.RESET}"); game.is_connected = True; game.current_vm = game.machines[target]; game.remote_user="www-data"; game.current_vm.cwd="/var/www/hidden"
            else: print("Nothing found.")

        elif cmd == "ftp":
            if game.stage_idx == 1 and arg1 == target:
                print("Anonymous Login OK."); game.local_vm.files["/"]["id_rsa"] = "PRIVATE KEY"
                print(">> 'id_rsa' Downloaded.")
            else: print("Refused.")

        elif cmd == "hydra":
            game.update_trace(5)
            if arg1 == "-l" and arg3:
                if game.stage_idx == 1 and arg2 == "dr_mario":
                    loading_bar(1.5, "Brute-forcing"); print(f"{Color.GREEN}[SUCCESS] FTP Password: ftp_pass_123{Color.RESET}")
                else: print("Failed.")
            else: print("Usage: hydra -l [ID] [IP]")

        elif cmd == "hashcat":
            if game.stage_idx == 1 and arg1 == "5f4dcc3b5aa765d61d8327deb882cf99":
                loading_bar(2.0, "Cracking"); print(f"{Color.GREEN}[CRACKED] password{Color.RESET}")
            else: print("Hash invalid or failed.")

        elif cmd == "searchsploit":
            if game.stage_idx == 3 and "nginx" in str(arg1):
                print(f"{Color.GREEN}[+] Exploit Found! Creds: admin / dragon123{Color.RESET}")
            else: print("No result.")

        elif cmd == "metasploit":
            if game.stage_idx == 4:
                loading_bar(2.0, "Zero-Day"); print(f"{Color.GREEN}>> ROOT ACCESS{Color.RESET}"); game.is_connected = True; game.current_vm = game.machines[target]; game.remote_user="root"; game.current_vm.cwd="/root/secret"
            else: print("Not needed.")

        elif cmd == "chmod":
            if arg1 == "600" and arg2 == "id_rsa":
                print("Permissions set to 600 (User R/W only). Key is secure."); game.local_vm.file_perms["/id_rsa"] = "600"
            else: print("Usage: chmod 600 [file]")

        elif cmd == "ssh":
            if arg1 == "-i" and arg2 == "id_rsa": # Key auth
                parts_ip = arg3.split("@")
                if len(parts_ip) > 1 and parts_ip[1] == target:
                    if game.local_vm.file_perms.get("/id_rsa") == "600":
                        print(f"{Color.GREEN}>> Logged In via Key.{Color.RESET}"); game.is_connected = True; game.current_vm = game.machines[target]; game.remote_user = parts_ip[0]; game.current_vm.cwd = "/home/dr_mario"
                    else: print(f"{Color.RED}Error: Private key 0644 is too open. Use chmod.{Color.RESET}")
                else: print("Target error.")
            elif "@" in arg1: # Password auth
                u, i = arg1.split("@")
                if i == target:
                    pw = input("Password: ")
                    if (i == "10.0.0.1" and pw == "1234") or (i == "10.20.30.40" and pw == "dragon123"):
                        print("Logged In."); game.is_connected = True; game.current_vm = game.machines[i]; game.remote_user = u
                        if u == "admin": game.current_vm.cwd = "/home/admin"
                    else: print("Login Failed.")
                else: print("Unknown Host.")
            else: print("Usage: ssh [ID]@[IP] or ssh -i [Key] [ID]@[IP]")
        
        elif cmd in ["ls", "cat"]: sys_cmd(game, cmd, arg1)
        else: print("Error.")

    # Remote
    else:
        if cmd in ["ls", "cd", "cat"]: sys_cmd(game, cmd, arg1)
        elif cmd == "ps":
            print("PID\tPROCESS")
            for pid, name in game.current_vm.processes.items(): print(f"{pid}\t{name}")
        elif cmd == "kill":
            if game.stage_idx == 2:
                pid = int(arg1)
                if pid == 102:
                    print("Watchdog killed."); game.stage_flags['killed_watchdog'] = True
                elif pid == 101:
                    if game.stage_flags['killed_watchdog']:
                        print("Locker killed."); game.stage_flags['killed_locker'] = True
                    else:
                        print(f"{Color.RED}[ALERT] Watchdog restarted process 101!{Color.RESET}")
                else: print("Bad PID.")
        
        elif cmd == "edit_log":
            if game.stage_idx == 3:
                ip = input("Enter IP to frame: ")
                if ip == "203.11.22.33":
                    print(">> Logs Framed."); game.stage_flags['framed_ip'] = True
                else: print("Wrong IP. Check mail.")
            else: print("Logs cleared.")

        elif cmd == "grep":
            if game.stage_idx == 4 and arg1 == "ledger" and arg2 == "*":
                print("Searching..."); time.sleep(1); print(f"{Color.GREEN}Match found: ledger_final_v2.xlsx{Color.RESET}")
            else: print("No matches.")

        elif cmd == "scp":
            if game.current_vm.get_file_content(arg1): print("Downloaded."); game.check_mission(arg1, "steal")
            else: print("File not found.")
        elif cmd == "decrypt":
            if game.stage_idx == 2 and game.stage_flags['killed_locker']:
                print("Decrypted."); game.check_mission("patient_data.enc", "decrypt")
            else: print("Error or Daemon active.")
        elif cmd == "shred":
            if game.stage_idx == 3 and game.stage_flags['framed_ip']:
                print("Shredding..."); game.check_mission(arg1, "shred")
            else: print("Error or Logs not framed.")
        elif cmd == "webcam_snap":
            if game.stage_idx == 4: print("Captured."); game.check_mission("j.jpg", "webcam")
        
        else: print("Error.")

def sys_cmd(game, cmd, arg):
    vm = game.current_vm
    if cmd == "ls":
        f, d = vm.list_files()
        if game.stage_idx == 4 and vm.cwd == "/root/secret":
            print("data_001.dat  data_002.dat ... (100 files) ... use 'grep' to find.")
        else:
            print("  ".join([f"{Color.BLUE}{x}/{Color.RESET}" for x in d] + f))
    elif cmd == "cd": vm.change_dir(arg)
    elif cmd == "cat":
        c = vm.get_file_content(arg)
        print(f"--- {arg} ---\n{c}" if c else "File not found")