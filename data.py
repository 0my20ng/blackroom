from models import VirtualMachine

def get_initial_data():
    local_vm = VirtualMachine("Localhost", "127.0.0.1", 
                                   files={"/": {"manual.txt": "Type 'man' to read", "contract_j.txt": "J takes 70%, You take 30%."}})
    
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

    machines = {"10.0.0.1": vm_tut, "192.168.10.5": vm_bio, "45.33.22.11": vm_ran, "10.20.30.40": vm_cloud, "172.16.99.99": vm_apex}

    stages_info = [
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
    
    return local_vm, machines, stages_info
