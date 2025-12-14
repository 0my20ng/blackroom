from models import VirtualMachine

MANUAL = {
    "nmap": "사용법: nmap [IP]\n설명: [정찰] 타겟 서버의 열려있는 포트와 서비스를 확인합니다.",
    "web_scan": "사용법: web_scan [IP]\n설명: [정찰] 웹 페이지를 분석하여 숨겨진 정보나 ID를 수집합니다.",
    "analyze": "사용법: analyze [IP] [Port]\n설명: [분석] 포트의 상세 정보를 확인합니다.",
    "searchsploit": "사용법: searchsploit [서비스명]\n설명: [분석] 취약점을 검색합니다.",
    
    "hydra": "사용법: hydra -l [ID] [IP]\n설명: [공격] FTP/SSH 비밀번호를 크랙합니다.",
    "hashcat": "사용법: hashcat [해시값]\n설명: [해독] 암호화된 해시를 풉니다.",
    "metasploit": "사용법: metasploit\n설명: [공격] 시스템 강제 침투.",
    
    "ssh": "사용법: ssh [ID]@[IP] (옵션: -i [키파일])\n설명: 원격 접속. 키 파일 사용 시 -i 옵션 필요.",
    "ftp": "사용법: ftp [IP]\n설명: 파일 서버 접속.",
    
    "ls": "파일 목록", "cat": "파일 읽기", "cd": "폴더 이동",
    "ps": "프로세스 목록 확인 (PID)", 
    "kill": "사용법: kill [PID]\n설명: 프로세스 강제 종료.",
    "chmod": "사용법: chmod [권한] [파일]\n설명: 파일 권한 변경 (예: chmod 600 key).",
    "grep": "사용법: grep [검색어] *\n설명: 현재 폴더의 모든 파일에서 특정 단어를 찾습니다.",
    "run": "사용법: ./[파일]\n설명: 스크립트 실행.",
    
    "scp": "파일 다운로드", "decrypt": "복호화",
    "edit_log": "로그 조작 (IP 입력 필요)",
    "webcam_snap": "증거 확보",
    "email": "미션 확인", "hint": "힌트"
}

def setup_machines():
    # 0. Tutorial VM (Restored)
    vm_tut = VirtualMachine("Test_Server", "10.0.0.1", 
                            files={"/": {"hello.txt": "Welcome agent.", "j_memo.log": "Subject #404: Skill level low. Disposable asset."}},
                            users={"guest": "1234"},
                            ports=["22/tcp"], services={"22": "OpenSSH (Weak Password)"})

    # 1. Stage 1 (BioTech)
    vm_bio = VirtualMachine("BioTech", "192.168.10.5",
                            files={
                                "/": {"readme.txt": "FTP Server v2.0"}, 
                                "/pub": {"id_rsa": "BEGIN OPENSSH PRIVATE KEY..."}, # SSH 키
                                "/home/dr_mario": {"formula_x.pdf": "CONFIDENTIAL DATA"}
                            },
                            users={"dr_mario": "ftp_pass_123"}, # FTP 비번
                            ports=["21/tcp", "22/tcp", "80/tcp"], 
                            services={"21": "vsftpd", "22": "OpenSSH", "80": "Apache (Company Info)"})
    vm_bio.dirs["/"] = ["pub", "home"]; vm_bio.dirs["/home"] = ["dr_mario"]
    vm_bio.file_perms["/pub/id_rsa"] = "644" 

    # 2. Stage 2 (Ransom)
    vm_ran = VirtualMachine("Ransom_C2", "45.33.22.11",
                            files={"/var/www/hidden": {
                                "master_key.txt": "key: money_is_king",
                                "patient_data.enc": "[LOCKED]"
                            }},
                            users={}, ports=["80/tcp"], services={"80": "Apache (Vuln)"},
                            processes={101: "locker_daemon", 102: "watchdog_service"}) 
    
    # 3. Stage 3 (CyberCloud)
    vm_cloud = VirtualMachine("CyberCloud", "10.20.30.40",
                              files={
                                  "/home/admin": {"source_code.zip": "Code", "server.log": "Access Log"},
                                  "/var/mail": {"inbox": "From: S-Corp (IP: 203.11.22.33)\nSubject: We will destroy you."}
                              },
                              users={"admin": "dragon123"},
                              ports=["22/tcp", "80/tcp"], services={"80": "nginx", "22": "OpenSSH"})
    vm_cloud.dirs["/"] = ["home", "var"]; vm_cloud.dirs["/home"] = ["admin"]; vm_cloud.dirs["/var"] = ["mail"]

    # 4. Stage 4 (Apex)
    secret_files = {f"data_{i:03d}.dat": "Encrypted junk" for i in range(1, 100)}
    secret_files["ledger_final_v2.xlsx"] = "J's Secret Ledger"
    
    vm_apex = VirtualMachine("Apex_Main", "172.16.99.99",
                             files={"/root/secret": secret_files},
                             users={"root": "0day"},
                             ports=["Firewall"], services={"Firewall": "Active"})
    
    # Return all machines
    return {
        "10.0.0.1": vm_tut,
        "192.168.10.5": vm_bio, 
        "45.33.22.11": vm_ran, 
        "10.20.30.40": vm_cloud, 
        "172.16.99.99": vm_apex
    }

def get_stages_info():
    return [
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
            "email_sub": "계약 01: B사 신약 데이터",
            "email_sender": "J (Broker)",
            "beginner": """B사(192.168.10.5)다. 3단계로 뚫어라.
1. 'web_scan'으로 홈페이지를 털어서 직원 ID를 찾아내.
2. 찾아낸 ID로 'hydra'를 써서 FTP 비밀번호를 크랙해.
3. FTP에 접속해서 'id_rsa'(SSH í‚¤)를 ‹¤ìš´ë¡œë“œí•´.
4. ì¤‘ìš”: ë‹¤ìš´ë°›ì € í‚¤ëŠ” ê¶Œí•œì ´ ë„ˆë¬´ ì—´ë ¤ìžˆìœ¼ë©´ ëª» ì ¨. 'chmod 600 id_rsa'ë¡œ ìž ê°€.
5. 'ssh -i id_rsa [ID]@192.168.10.5'ë¡œ ì ‘ì† í•´ì„œ íŒŒì ¼ì „ í›”ì³ .""",
            "expert": """B사(192.168.10.5)다.
웹사이트(80)에 직원 정보가 있을 거다. 그걸로 FTP(21)를 뚫어.
FTP에 SSH 접속용 **비밀키(Key)**가 있다는데, 권한(Permission) 설정 조심하고.
**chmod** 알지?""",
            "news": ">> [경제] B제약, 서버 관리자 키 유출로 기밀 도난... 보안 불감증 논란."
        },
        {
            "target": "45.33.22.11", "goal": "patient_data.enc", "reward": 3000, "name": "Ransom Decrypt",
            "email_sub": "계약 02: 프로세스 퍼즐",
            "email_sender": "J (Broker)",
            "beginner": """병원 랜섬웨어 건이다(45.33.22.11).
1. 'web_scan'으로 키를 찾고 자동 접속.
2. 'ps'로 프로세스를 봐. 놈들이 감시자(watchdog)를 심어놨어.
3. 'kill' 순서가 틀리면 프로세스가 되살아난다. 
   감시자(102)를 먼저 죽이고, 그 다음 락커(101)를 죽여.
4. 다 죽이고 'decrypt patient_data.enc [키]'.""",
            "expert": """랜섬웨어 C2(45.33.22.11)다.
접속 후엔 프로세스 관리가 핵심이야. 
**Watchdog** 프로세스가 살아있으면 아무리 악성코드를 죽여도 부활할 거다.
순서를 잘 생각해.""",
            "news": ">> [사회] '좀비 프로세스' 완벽 제압... 병원 시스템 정상화."
        },
        {
            "target": "10.20.30.40", "goal": "source_code.zip", "reward": 5000, "name": "Cyber Sabotage",
            "email_sub": "계약 03: 내부자 위장",
            "email_sender": "J (Broker)",
            "beginner": """C사(10.20.30.40)를 파괴하되, 남에게 뒤집어씌워야 해.
1. 'searchsploit nginx' -> SSH 접속 정보 획득.
2. 접속 후 '/var/mail' 폴더로 가서 이메일('inbox')을 읽어.
3. 우리에게 적대적인 경쟁사(S-Corp)의 IP가 메일에 있을 거야.
4. 'edit_log'를 실행하고 그 경쟁사 IP를 입력해. (이게 핵심이다)
5. 그 다음 'shred source_code.zip'.""",
            "expert": """C사(10.20.30.40) 건이다.
SQL Injection으로 뚫고 들어가.
그냥 지우지 말고, 관리자 메일함을 뒤져서 **경쟁사 IP**를 알아내.
그 IP로 **로그를 위조(edit_log)**한 뒤에 날려버려.""",
            "news": ">> [IT] C사 데이터 파괴 사건, 경쟁사 S-Corp 소행으로 밝혀져... 경찰 수사 착수."
        },
        {
            "target": "172.16.99.99", "goal": "ledger_final_v2.xlsx", "reward": 0, "name": "The Betrayal",
            "email_sub": "경고: J를 추적하라",
            "email_sender": "UNKNOWN",
            "beginner": """J가 배신했다. 172.16.99.99.
1. 'nmap -Pn 172.16.99.99' -> 'metasploit'으로 뚫어.
2. '/root/secret'에 들어가면 파일이 100개가 넘을 거야.
3. 'ls'로는 못 찾는다. 'grep ledger *' 명령어로 진짜 장부를 찾아.
4. 찾은 파일명으로 'scp' 하고, 'webcam_snap'으로 마무리해.""",
            "expert": """J가 널 팔아넘겼다. (172.16.99.99)
**nmap -Pn**과 **metasploit**을 써.
놈이 데이터 더미 속에 진짜 장부를 숨겨놨을 거다.
**grep** 명령어로 찾아내.""",
            "news": ">> [속보] 국제 해커 중개상 J 체포. 익명의 제보자가 결정적 증거 제출."
        }
    ]

def get_init_local_files():
    return {"/": {"manual.txt": "Read me", "todo.txt": "1. Get Rich\n2. Survive"}}