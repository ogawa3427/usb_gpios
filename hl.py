import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import subprocess
import psutil
import threading

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.last_run = 0
        self.cooldown = 0.5  # クールダウン時間を0.5秒に短縮
        self.current_process = None
        self.exeC_file = None

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
            self.restart_program(self.exeC_file)

    def restart_program(self, exeC_file):
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
                [sys.executable, exeC_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1  # ラインバッファリングを設定
            )
            
            # 出力監視用の関数
            def monitor_output(pipe, is_error=False):
                for line in pipe:
                    if is_error:
                        print(line.strip(), file=sys.stderr, flush=True)
                    else:
                        print(line.strip(), flush=True)

            # 標準出力と標準エラー出力を別々のスレッドで監視
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

def watch_file(file_path, exeC_file):
    event_handler = CodeChangeHandler(file_path)
    event_handler.exeC_file = exeC_file
    observer = Observer()
    
    # ファイルの親ディレクトリを監視
    directory = os.path.dirname(os.path.abspath(file_path))
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    # 初回実行
    event_handler.restart_program(exeC_file)

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
    if len(sys.argv) != 3:
        print("使用方法: python hot_reloader.py <視対象のPythonァイル> <実行ファイル>")
        sys.exit(1)

    target_file = sys.argv[1]
    exeC_file = sys.argv[2]
    if not os.path.exists(target_file):
        print(f"エラー: ファイル '{target_file}' が見つかりません")
        sys.exit(1)
   
    if not os.path.exists(exeC_file):
        print(f"エラー: ファイル '{exeC_file}' が見つかりません")
        sys.exit(1)

    watch_file(target_file, exeC_file)