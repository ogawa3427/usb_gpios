#include <M5Unified.h>
#include "env.h"

void setup() {
  USBSerial.begin(115200);
  auto cfg = M5.config();
  M5.begin(cfg);
  M5.Lcd.setTextSize(4);
  M5.Lcd.setFont(&fonts::Font2);
}

void loop() {
  if (USBSerial.available()) {
    String receivedString = USBSerial.readStringUntil('\n');
    uint8_t receivedByte = receivedString.toInt();
    // USBSerial.println(receivedByte);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.printf("%02X", receivedByte);
  }
}

