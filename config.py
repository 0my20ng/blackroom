import os

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
