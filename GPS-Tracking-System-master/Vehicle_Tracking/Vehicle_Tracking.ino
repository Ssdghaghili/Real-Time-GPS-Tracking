#include <SoftwareSerial.h>
SoftwareSerial gpsSerial(10, 11);  // RX, TX

String nmeaLine = "";

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
  Serial.println("Reading GPS Data...");
}

void loop() {
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    if (c == '\n') {
      if (nmeaLine.startsWith("$GPGGA")) {
        parseGPGGA(nmeaLine);
      }
      nmeaLine = "";
    } else {
      nmeaLine += c;
    }
  }
}

void parseGPGGA(String sentence) {
  // نمونه: $GPGGA,132833.000,3547.1854,N,05127.2570,E,...
  int commaIndex = 0;
  int fieldIndex = 0;
  String fields[15];

  for (int i = 0; i < sentence.length(); i++) {
    if (sentence.charAt(i) == ',' || sentence.charAt(i) == '*') {
      fields[fieldIndex++] = sentence.substring(commaIndex, i);
      commaIndex = i + 1;
    }
  }

  if (fields[2].length() > 0 && fields[4].length() > 0) {
    float lat = convertToDecimal(fields[2].toFloat(), fields[3]);
    float lon = convertToDecimal(fields[4].toFloat(), fields[5]);

    Serial.print("📍 Latitude: ");
    Serial.println(lat, 6);
    Serial.print("📍 Longitude: ");
    Serial.println(lon, 6);
    Serial.println("----------------------");
  }
}

float convertToDecimal(float raw, String direction) {
  int degrees = int(raw / 100);
  float minutes = raw - (degrees * 100);
  float decimal = degrees + (minutes / 60.0);

  if (direction == "S" || direction == "W") {
    decimal *= -1;
  }
  return decimal;
}