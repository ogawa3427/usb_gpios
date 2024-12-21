import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import subprocess
import psutil

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.last_run = 0
        self.cooldown = 0.5  # クールダウン時間を0.5秒に短縮
        self.current_process = None

    def on_modified(self, event):
        # イベントがFileModifiedEventであることを確認
        if not isinstance(event, FileModifiedEvent):
            return

        # パスが監視対象のファイルと一致するか確認
        if os.path.abspath(event.src_path) != self.file_path:
            return

        current_time = time.time()
        if current_time - self.last_run >= self.cooldown:
            self.last_run = current_time
            self.restart_program()

    def restart_program(self):
        print("\n" + "="*50)
        print(f"変更を検知: {self.file_path}")
        
        # 既存のプロセスを終了
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

        # 新しいプロセスを開始
        try:
            self.current_process = subprocess.Popen(
                [sys.executable, self.file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
        except Exception as e:
            print(f"実行エラー: {e}")

def watch_file(file_path):
    event_handler = CodeChangeHandler(file_path)
    observer = Observer()
    
    # ファイルの親ディレクトリを監視
    directory = os.path.dirname(os.path.abspath(file_path))
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    # 初回実行
    event_handler.restart_program()

    print(f"ファイル監視を開始: {file_path}")
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
    if len(sys.argv) != 2:
        print("使用方法: python hot_reloader.py <監視対象のPythonファイル>")
        sys.exit(1)

    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print(f"エラー: ファイル '{target_file}' が見つかりません")
        sys.exit(1)

    watch_file(target_file)