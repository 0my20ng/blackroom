import sys
import ui
from config import Color, MANUAL

# Command logic helpers
def get_arg(parts, index):
    return parts[index] if len(parts) > index else None

def execute_command(game, command_str):
    parts = command_str.split()
    if not parts: return
    
    cmd = parts[0].lower()
    arg1 = get_arg(parts, 1)
    arg2 = get_arg(parts, 2)
    arg3 = get_arg(parts, 3)
    
    # Common command check for mail read
    if not game.mail_read and cmd != "email" and cmd != "exit":
        print(f"{Color.YELLOW}You have unread mail from J. Type 'email'.{Color.RESET}")
        return

    # Global Commands
    if cmd == "email":
        game.draw_email()
        return
    elif cmd == "exit":
        if game.is_connected:
            game.is_connected = False
            game.current_vm = game.local_vm
            game.remote_user = "ghost"
            print("Disconnected.")
        else:
            sys.exit()
        return
    elif cmd == "help":
        print(f"{Color.CYAN}Commands: email, nmap, analyze, ssh, ftp, hydra, hashcat, web_scan, searchsploit, sqlmap, metasploit, ps, kill, chmod, ./run, ls, cat, scp, decrypt, shred, edit_log{Color.RESET}")
        return
    elif cmd == "man":
        if arg1 and arg1 in MANUAL:
            print(f"{Color.BLUE}{MANUAL[arg1]}{Color.RESET}")
        else:
            print("Usage: man [command]")
        return
    elif cmd == "status":
        ui.draw_ui_box([f"Trace: {game.trace_rate:.1f}%", f"Money: ${game.money}"], title=" STATUS ")
        return
    elif cmd == "hint":
        game.provide_hint()
        return

    # Dispatch based on connection state
    if not game.is_connected:
        _execute_local(game, cmd, arg1, arg2, arg3)
    else:
        _execute_remote(game, cmd, arg1, arg2)

def _execute_local(game, cmd, arg1, arg2, arg3):
    target = game.stages_info[game.stage_idx]['target']
    
    if cmd == "nmap":
        game.update_trace(2)
        if arg1 == target or (game.stage_idx == 4 and arg1 == "-Pn"):
            ui.loading_bar(1.0, "Scanning")
            if target in game.machines:
                for p in game.machines[target].ports:
                    print(f"{Color.GREEN}[+] {p} open{Color.RESET}")
            else:
                print("Error: IP not found.")
        else:
            print("Target unreachable.")

    elif cmd == "analyze":
        game.update_trace(2)
        if arg1 == target and arg2:
            ui.loading_bar(0.8, "Analyzing")
            print(f"{Color.GREEN}>> {game.machines[target].services.get(arg2, 'Unknown')}{Color.RESET}")
        else:
            print("Usage: analyze [IP] [Port]")

    elif cmd == "searchsploit":
        if game.stage_idx == 3 and arg1 and "nginx" in arg1.lower():
            print(f"{Color.GREEN}[+] Exploit Found! Creds: ssh admin@10.20.30.40 (pw: dragon123){Color.RESET}")
        else:
            print("No exploit found.")

    elif cmd == "hashcat":
        game.update_trace(3)
        if game.stage_idx == 1 and arg1 == "5f4dcc3b5aa765d61d8327deb882cf99":
            ui.loading_bar(2.0, "Cracking")
            print(f"{Color.GREEN}[CRACKED] password{Color.RESET}")
        else:
            print("Hash invalid or failed.")

    elif cmd == "ftp":
        if arg1 == target and game.stage_idx == 1:
            print("Anonymous Login OK.")
            game.local_vm.files["/"]["staff_hash.txt"] = "dr_mario:5f4dcc3b5aa765d61d8327deb882cf99"
            print(">> Downloaded.")
        else:
            print("Refused.")

    elif cmd == "hydra":
        game.update_trace(5)
        if arg1 == "-l" and arg3:
            target_vm = game.machines.get(arg3)
            if target_vm:
                ui.loading_bar(1.5, "Brute-forcing")
                found = False
                for u, pw in target_vm.users.items():
                    if u.lower() == arg2.lower():
                        print(f"{Color.GREEN}[SUCCESS] PW: {pw}{Color.RESET}")
                        found = True
                        break
                if not found:
                    print("Failed.")
            else:
                print("Bad IP.")
        else:
            print("Usage: hydra -l [ID] [IP]")

    elif cmd == "web_scan":
        if arg1 == target and game.stage_idx == 2:
            ui.loading_bar(1.5, "Scanning")
            print(f"{Color.GREEN}[+] Key Found.{Color.RESET}")
            game.is_connected = True
            game.current_vm = game.machines[target]
            game.remote_user = "www-data"
            game.current_vm.cwd = "/var/www/hidden"
        else:
            print("Nothing.")

    elif cmd == "sqlmap":
        print("Use 'searchsploit' instead.")

    elif cmd == "metasploit":
        if game.stage_idx == 4:
            ui.loading_bar(2.0, "Zero-Day Attack")
            print(f"{Color.GREEN}>> ROOT ACCESS{Color.RESET}")
            game.is_connected = True
            game.current_vm = game.machines[target]
            game.remote_user = "root"
            game.current_vm.cwd = "/root/secret"
        else:
            print("Not needed.")

    elif cmd == "ssh":
        if arg1 and "@" in arg1:
            u, i = arg1.split("@")
            if i in game.machines:
                pw = input("Password: ")
                if (i == "192.168.10.5" and pw == "password") or \
                   (i == "10.20.30.40" and pw == "dragon123") or \
                   (i == "10.0.0.1" and pw == "1234"):
                    game.is_connected = True
                    game.current_vm = game.machines[i]
                    game.remote_user = u
                    print("Logged In.")
                    if u == "dr_mario": game.current_vm.cwd = "/home/dr_mario"
                    elif u == "admin": game.current_vm.cwd = "/home/admin"
                else:
                    print("Login Failed.")
                    game.update_trace(5)
            else:
                print("Unknown Host.")
        else:
            print("Usage: ssh [user]@[IP]")

    elif cmd in ["ls", "cat"]:
        _sys_cmd(game, cmd, arg1)
    else:
        print("Error.")

def _execute_remote(game, cmd, arg1, arg2):
    if cmd in ["ls", "cd", "cat"]:
        _sys_cmd(game, cmd, arg1)
    elif cmd == "ps":
        print("PID\tPROCESS")
        for pid, name in game.current_vm.processes.items():
            print(f"{pid}\t{name}")
    elif cmd == "kill":
        if game.stage_idx == 2 and arg1 == "882":
            print("Killed.")
            game.stage_flags['killed_daemon'] = True
        else:
            print("Bad PID.")
    elif cmd == "chmod":
        if arg1 == "+x" and arg2 == "wiper.sh":
            print("Permission Granted.")
        else:
            print("Usage: chmod +x [file]")
    elif cmd == "./wiper.sh":
        if game.stage_idx == 3:
            print("Wiping...")
            game.stage_flags['wiped'] = True
            game.check_mission("wiper", "shred")
        else:
            print("Denied.")
    elif cmd == "scp":
        if game.current_vm.get_file_content(arg1):
            print("Downloaded.")
            game.check_mission(arg1, "steal")
        else:
            print("File not found.")
    elif cmd == "decrypt":
        if game.stage_idx == 2:
            if game.stage_flags['killed_daemon']:
                print("Decrypted.")
                game.check_mission("patient_data.enc", "decrypt")
            else:
                print(f"{Color.RED}[ERROR] Daemon active!{Color.RESET}")
                game.update_trace(10)
        else:
            print("Error.")
    elif cmd == "edit_log":
        ui.loading_bar(1.0, "Modifying Logs")
        print(">> Logs Framed.")
    elif cmd == "shred":
        if game.stage_idx == 3:
            print("Warning: Use the wiper script.")
        else:
            print("Shredding...")
    elif cmd == "webcam_snap":
        if game.stage_idx == 4:
            print(">> Captured.")
            game.check_mission("j.jpg", "webcam")
    else:
        print("Error.")

def _sys_cmd(game, cmd, arg):
    vm = game.current_vm
    if cmd == "ls":
        f, d = vm.list_files()
        print("  ".join([f"{Color.BLUE}{x}/{Color.RESET}" for x in d] + f))
    elif cmd == "cd":
        vm.change_dir(arg)
    elif cmd == "cat":
        c = vm.get_file_content(arg)
        if c:
            color = Color.MAGENTA if "J" in c or "Broker" in c else Color.WHITE
            print(color + f"--- {arg} ---\n{c}" + Color.RESET)
        else:
            print("File not found")
