#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <DHT.h>

#define DHTTYPE DHT22

uint8_t DHTPin = D4;
DHT dht(DHTPin, DHTTYPE);

float temperature;
float humidity;

const char* ssid = "YOUR_WIFI";
const char* password = "secret wifi password";

const char* serverName = "http://sensorhub:8000/sensors/api/data/interior";
const char* json = "{\"temperatura\":%.02f,\"umidade\":%.02f}";

unsigned long lastTime = 0;
unsigned long timerDelay = 60000;
char requestBody[50];

void setup() {
  pinMode(DHTPin, INPUT);
  dht.begin();
  
  Serial.begin(115200);
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

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    if (WiFi.status() == WL_CONNECTED) {
      temperature = dht.readTemperature();
      humidity = dht.readHumidity(); 

      HTTPClient http;
      
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");
      snprintf(requestBody, 50, json, temperatura, umidade);
      int httpResponseCode = http.POST(requestBody);
      http.end();

      Serial.println(requestBody);
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
