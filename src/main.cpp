#include "env.h"

void setup() {
  Serial.begin(115200);
}

void loop() {
  String inputString = "";
  while (Serial.available()) {
    inputString += (char)Serial.read();
  }
  Serial.println(inputString);
}

