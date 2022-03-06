/*
             Vcc    to 3.3v
             GND    to GND
             D4     to SDA/SDATA
             D5     to SCL/SCK/SCLOCK
*/
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Adafruit_BMP280.h>
#include <Wire.h>

/* ##### PRESSURE SENSOR THINGS ##### */
int PRESSURE_SENSOR_ADDRESS = 0x76;

Adafruit_BMP280 bmp;

float pressure;
/* ### END PRESSURE SENSOR THINGS ### */

/* ####### NETWORK THINGS ####### */
const char* ssid = "YOUR_WIFI";
const char* password = "secret wifi password";

const char* serverName = "http://sensorhub:8000/sensors/api/data/pressao";
const char* json = "{\"pressao\":%.02f}";

char requestBody[50];
/* ##### END NETWORK THINGS ##### */

unsigned long lastTime = 0;
unsigned long timerDelay = 60000;

void setup_wifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void setup_pressure_sensor() {
  Wire.begin(D4, D5); //D4 = SDA, D5 = SCL
  while (!bmp.begin(PRESSURE_SENSOR_ADDRESS)) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring!"));
    delay(500);
    Serial.print(".");
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  Serial.println("");
  Serial.println("Pressure sensor ready");
}

void send_pressure(float pressao) {
  HTTPClient http;

  http.begin(serverName);
  http.addHeader("Content-Type", "application/json");
  snprintf(requestBody, 50, json, pressao);
  int httpResponseCode = http.POST(requestBody);
  http.end();

  Serial.println(requestBody);
  Serial.print("Response: ");
  Serial.println(httpResponseCode);
}

void send_data() {
  pressure = bmp.readPressure();
  if (isnan(pressao)) return;

  pressao = pressao/100;
  send_pressure(pressao);
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  setup_pressure_sensor();
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    if (WiFi.status() == WL_CONNECTED) {
      send_data();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}