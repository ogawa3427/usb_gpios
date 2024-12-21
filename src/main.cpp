#include <M5Unified.h>
#include "env.h"

void setup() {
  USBSerial.begin(115200);
  auto cfg = M5.config();
  M5.begin(cfg);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setFont(&fonts::Font2);
}

void loop() {
  if (USBSerial.available()) {
    String receivedString = USBSerial.readStringUntil('\n');
    receivedString.trim();
    
    // uint8_t receivedByte = receivedString.toInt();
    // USBSerial.println(receivedByte);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.fillScreen(BLACK);

    uint32_t value = strtoul(receivedString.c_str(), NULL, 16);  // 16進数として解析
    M5.Lcd.printf("%02X", value);
    if ((receivedString.toInt() & 0xFF00) == 0x1200) {
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.printf("pinMode");
      int pin = (receivedString.toInt() & 0x000F);  // ピン番号を取得（4ビット右シフト）
      pinMode(pin, OUTPUT);   // 下位バイトのみを取得
    } 
    else if ((receivedString.toInt() & 0xFF00) == 0x1100) {
      M5.Lcd.setCursor(0, 0);
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.printf("dWrite");
      int pin = (receivedString.toInt() & 0x000F);  // ピン番号を取得（4ビット右シフト）
      int value = (receivedString.toInt() & 0x0010) >> 4;       // 値を取得（最下位ビット）
      M5.Lcd.printf("pin: %d, value: %d", pin, value);
      digitalWrite(pin, value);
    }

    
    
  }
}

