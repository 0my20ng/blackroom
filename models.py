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
