from serial import Serial
import usb_gpios

# 開発環境かどうかのフラグ（環境変数などで管理することを推奨）
DEV_MODE = True

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
    ser = Serial(port='COM3', baudrate=115200)

m5atoms3 = usb_gpios.M5(usb_gpios.M5.Boards.M5_ATOMS3, ser)

m5atoms3.digitalWrite(1, 1)