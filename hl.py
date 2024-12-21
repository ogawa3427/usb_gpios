import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import subprocess
import psutil
import threading

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, file_paths):
        self.file_paths = [os.path.abspath(path) for path in file_paths]
        self.last_run = 0
        self.cooldown = 0.5
        self.current_process = None
        self.exeC_file = None

    def on_modified(self, event):
        if not isinstance(event, FileModifiedEvent):
            return

        if os.path.abspath(event.src_path) not in self.file_paths:
            return

        current_time = time.time()
        if current_time - self.last_run >= self.cooldown:
            self.last_run = current_time
            self.restart_program(self.exeC_file)

    def restart_program(self, exeC_file):
        print("\n" + "="*50)
        print(f"変更を検知: {', '.join(self.file_paths)}")
        
        if self.current_process:
            try:
                process = psutil.Process(self.current_process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
            except (psutil.NoSuchProcess, ProcessLookupError):
                pass

        print("プログラムを再実行します...")
        print("="*50 + "\n")

        try:
            self.current_process = subprocess.Popen(
                [sys.executable, exeC_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            def monitor_output(pipe, is_error=False):
                for line in pipe:
                    if is_error:
                        print(line.strip(), file=sys.stderr, flush=True)
                    else:
                        print(line.strip(), flush=True)

            stdout_thread = threading.Thread(
                target=monitor_output, 
                args=(self.current_process.stdout,),
                daemon=True
            )
            stderr_thread = threading.Thread(
                target=monitor_output, 
                args=(self.current_process.stderr, True),
                daemon=True
            )
            
            stdout_thread.start()
            stderr_thread.start()
                
        except Exception as e:
            print(f"実行エラー: {e}")

def watch_file(file_paths, exeC_file):
    event_handler = CodeChangeHandler(file_paths)
    event_handler.exeC_file = exeC_file
    observer = Observer()
    
    watched_dirs = set(os.path.dirname(os.path.abspath(path)) for path in file_paths)
    for directory in watched_dirs:
        observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    event_handler.restart_program(exeC_file)

    print(f"ファイル監視を開始: {', '.join(file_paths)}")
    print("終了するには Ctrl+C を押してください...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.current_process:
            try:
                process = psutil.Process(event_handler.current_process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
            except (psutil.NoSuchProcess, ProcessLookupError):
                pass
        print("\n監視を終了しました")
    
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法: python hot_reloader.py <監視対象のPythonファイル1> [<監視対象のPythonファイル2> ...] <実行ファイル>")
        sys.exit(1)

    target_files = sys.argv[1:-1]
    exeC_file = sys.argv[-1]

    for file_path in target_files + [exeC_file]:
        if not os.path.exists(file_path):
            print(f"エラー: ファイル '{file_path}' が見つかりません")
            sys.exit(1)

    watch_file(target_files, exeC_file)