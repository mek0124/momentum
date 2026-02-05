import requests
import zipfile
import shutil
import tempfile
import hashlib
from pathlib import Path
from PySide6.QtCore import QThread, Signal


class UpdateThread(QThread):
    progress_update = Signal(str, int)
    finished = Signal(bool, str)
    
    def __init__(self, root_dir, latest_version):
        super().__init__()
        self.root_dir = root_dir
        self.latest_version = latest_version
        self.temp_dir = None
        self.should_stop = False
    
    def calculate_file_hash(self, filepath):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def should_preserve_file(self, relative_path):
        """Check if file should be preserved (user data)"""
        preserve_patterns = [
            'app/storage/',
            '.env',
            'config.ini',
            'settings.json'
        ]
        
        path_str = str(relative_path)
        for pattern in preserve_patterns:
            if path_str.startswith(pattern):
                return True
        return False
    
    def get_release_files_info(self, release_folder):
        """Get file information from release"""
        files_info = {}
        all_files = list(release_folder.rglob('*'))
        total_files = len([f for f in all_files if f.is_file()])
        processed = 0
        
        for item in all_files:
            if self.should_stop:
                return {}
                
            if item.is_file():
                rel_path = item.relative_to(release_folder)
                file_hash = self.calculate_file_hash(item)
                files_info[str(rel_path)] = {
                    'path': item,
                    'hash': file_hash,
                    'size': item.stat().st_size
                }
                processed += 1
                
                if processed % 10 == 0:
                    progress = 40 + int(5 * (processed / total_files))
                    self.progress_update.emit(f"Analyzing release files...", progress)
        
        return files_info
    
    def get_current_files_info(self):
        """Get current files information"""
        files_info = {}
        ignore_patterns = ['__pycache__', '.git', '*.pyc', 'venv', 'backup_*']
        
        def should_ignore(path):
            for pattern in ignore_patterns:
                if pattern.startswith('*'):
                    if path.name.endswith(pattern[1:]):
                        return True
                elif pattern in path.name:
                    return True
            return False
        
        all_items = list(self.root_dir.rglob('*'))
        total_files = len([f for f in all_items if f.is_file() and not should_ignore(f)])
        processed = 0
        
        for item in all_items:
            if self.should_stop:
                return {}
                
            if item.is_file() and not should_ignore(item):
                rel_path = item.relative_to(self.root_dir)
                rel_str = str(rel_path)
                if not self.should_preserve_file(rel_str):
                    file_hash = self.calculate_file_hash(item)
                    files_info[rel_str] = {
                        'path': item,
                        'hash': file_hash,
                        'size': item.stat().st_size
                    }
                    processed += 1
                    
                    if processed % 10 == 0:
                        progress = 45 + int(5 * (processed / total_files))
                        self.progress_update.emit(f"Analyzing current files...", progress)
        
        return files_info
    
    def download_with_progress(self, download_url, zip_path):
        """Download file with progress updates"""
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if self.should_stop:
                    return False
                    
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        progress = 10 + int(20 * (downloaded / total_size))
                        self.progress_update.emit("Downloading update...", progress)
        
        return True
    
    def extract_with_progress(self, zip_path, extract_dir):
        """Extract zip with progress updates"""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.infolist()
            total_files = len(file_list)
            
            for i, file_info in enumerate(file_list):
                if self.should_stop:
                    return False
                    
                zip_ref.extract(file_info, extract_dir)
                
                if i % 10 == 0:
                    progress = 30 + int(10 * (i / total_files))
                    self.progress_update.emit("Extracting update...", progress)
        
        return True
    
    def run(self):
        try:
            self.progress_update.emit("Preparing update...", 5)
            
            repo_url = "https://github.com/mek0124/momentum"
            download_url = f"{repo_url}/archive/refs/tags/v{self.latest_version}.zip"
            
            self.temp_dir = tempfile.mkdtemp(prefix="momentum_update_")
            
            if self.should_stop:
                return
            
            self.progress_update.emit("Downloading update...", 10)
            
            zip_path = Path(self.temp_dir) / f"momentum-{self.latest_version}.zip"
            if not self.download_with_progress(download_url, zip_path):
                return
            
            if self.should_stop:
                return
            
            self.progress_update.emit("Extracting update...", 30)
            
            extract_dir = Path(self.temp_dir) / "extracted"
            if not self.extract_with_progress(zip_path, extract_dir):
                return
            
            if self.should_stop:
                return
            
            extracted_folder = next(extract_dir.iterdir())
            
            self.progress_update.emit("Analyzing changes...", 40)
            
            release_files = self.get_release_files_info(extracted_folder)
            if self.should_stop:
                return
            
            current_files = self.get_current_files_info()
            if self.should_stop:
                return
            
            files_to_update = []
            files_to_add = []
            files_to_remove = []
            
            self.progress_update.emit("Comparing versions...", 50)
            
            for rel_path, release_info in release_files.items():
                if self.should_stop:
                    return
                    
                if self.should_preserve_file(rel_path):
                    continue
                    
                if rel_path in current_files:
                    current_hash = current_files[rel_path]['hash']
                    release_hash = release_info['hash']
                    
                    if current_hash != release_hash:
                        files_to_update.append((rel_path, release_info['path']))
                else:
                    files_to_add.append((rel_path, release_info['path']))
            
            for rel_path, current_info in current_files.items():
                if self.should_stop:
                    return
                    
                if self.should_preserve_file(rel_path):
                    continue
                    
                if rel_path not in release_files:
                    files_to_remove.append(rel_path)
            
            total_operations = len(files_to_update) + len(files_to_add) + len(files_to_remove)
            if total_operations == 0:
                self.progress_update.emit("No changes needed!", 100)
                self.finished.emit(True, "Already up to date!")
                return
            
            self.progress_update.emit("Creating backup...", 60)
            
            backup_dir = self.root_dir / f"backup_v{self.latest_version}"
            if backup_dir.exists():
                shutil.rmtree(backup_dir, ignore_errors=True)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            for i, (rel_path, _) in enumerate(files_to_update):
                if self.should_stop:
                    return
                    
                source_file = self.root_dir / rel_path
                backup_file = backup_dir / rel_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(source_file, backup_file)
                except:
                    pass
                
                if i % 10 == 0:
                    progress = 60 + int(5 * (i / len(files_to_update)))
                    self.progress_update.emit(f"Backing up files...", progress)
            
            self.progress_update.emit("Applying updates...", 70)
            
            processed = 0
            for rel_path, source_path in files_to_update:
                if self.should_stop:
                    return
                    
                dest_path = self.root_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dest_path)
                processed += 1
                progress = 70 + int(10 * (processed / total_operations))
                self.progress_update.emit(f"Updating {rel_path}...", progress)
            
            for rel_path, source_path in files_to_add:
                if self.should_stop:
                    return
                    
                dest_path = self.root_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dest_path)
                processed += 1
                progress = 70 + int(10 * (processed / total_operations))
                self.progress_update.emit(f"Adding {rel_path}...", progress)
            
            for rel_path in files_to_remove:
                if self.should_stop:
                    return
                    
                dest_path = self.root_dir / rel_path
                try:
                    dest_path.unlink()
                    if dest_path.parent.exists() and not any(dest_path.parent.iterdir()):
                        dest_path.parent.rmdir()
                except:
                    pass
                processed += 1
                progress = 70 + int(10 * (processed / total_operations))
                self.progress_update.emit(f"Removing {rel_path}...", progress)
            
            self.progress_update.emit("Cleaning up...", 90)
            
            if self.temp_dir and Path(self.temp_dir).exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            
            self.progress_update.emit("Update complete!", 100)
            
            summary = f"Update completed!\n\n" \
                     f"Updated: {len(files_to_update)} files\n" \
                     f"Added: {len(files_to_add)} files\n" \
                     f"Removed: {len(files_to_remove)} files\n\n" \
                     f"User data preserved."
            self.finished.emit(True, summary)
            
        except Exception as e:
            if self.temp_dir and Path(self.temp_dir).exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.finished.emit(False, f"Update failed: {str(e)}")
    
    def terminate(self):
        self.should_stop = True
        super().terminate()