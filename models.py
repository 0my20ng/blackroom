class VirtualMachine:
    def __init__(self, name, ip, files=None, users=None, ports=None, services=None, processes=None):
        self.name = name
        self.ip = ip
        self.cwd = "/" 
        self.users = users if users else {} 
        self.ports = ports if ports else []
        self.services = services if services else {}
        self.processes = processes if processes else {} # {PID: "Name"}
        self.files = files if files else {"/": {}}
        self.file_perms = {} # {filepath: "644"} (기본 권한)
        self.dirs = {"/": []}
        
        # 파일 시스템 초기화 및 권한 설정
        for path, file_dict in self.files.items():
            if path not in self.dirs: self.dirs[path] = []
            for fname in file_dict:
                full_path = f"{path}/{fname}" if path != "/" else f"/{fname}"
                self.file_perms[full_path] = "644" # 기본 읽기 가능

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
        
        # 경로 보정 (// 제거)
        new_path = new_path.replace("//", "/")
        
        if new_path in self.files or new_path in self.dirs:
            self.cwd = new_path
            return True
        return False