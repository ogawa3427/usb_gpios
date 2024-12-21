import usb_gpios
import serial
import time
# 開発環境かどうかのフラグ（環境変数などで管理することを推奨）
DEV_MODE = False

if DEV_MODE:
    # 開発用のダミーシリアルクラス
    class DummySerial:
        def __init__(self, port=None, baudrate=None):
            self.port = port
            self.baudrate = baudrate
        
        def write(self, data):
            print(f"ダミー書き込み: {data}")
        
        def read(self, size=1):
            return b'\x00' * size
            
    ser = DummySerial(port='COM3', baudrate=115200)
else:
    # 本番用の実際のシリアル接続
    ser = serial.Serial(
        port='COM8',
        baudrate=115200,
        timeout=1,
        write_timeout=1
    )

m5atoms3 = usb_gpios.M5(usb_gpios.M5.Boards.M5_ATOMS3, ser)

def _setup():
    m5atoms3.pinMode(8, usb_gpios.M5.Peripheral.DIGITAL_OUTPUT)
    time.sleep(0.1)
    
sleepDelay = 1

def _loop():
    m5atoms3.digitalWrite(8, usb_gpios.M5.HIGH)
    time.sleep(sleepDelay)
    m5atoms3.digitalWrite(8, usb_gpios.M5.LOW)
    time.sleep(sleepDelay)

if __name__ == "__main__":
    _setup()
    while True:
        _loop()
