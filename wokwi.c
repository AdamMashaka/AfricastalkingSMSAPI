#include <WiFi.h>
#include <HTTPClient.h>
#include "DHTesp.h"
#include <LiquidCrystal_I2C.h>

#define I2C_ADDR    0x27
#define LCD_COLUMNS 20
#define LCD_LINES   4
const int DHT_PIN = 15;


const char* ssid = "Wokwi-GUEST";
const char* password = "";


const char* server = "https://f5b9-197-250-227-176.ngrok-free.app/send_sms";

DHTesp dhtSensor;
LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLUMNS, LCD_LINES);

void setup() {
  Serial.begin(115200);
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  lcd.init();
  lcd.backlight();


  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected!");
}

void loop() {
  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  Serial.println("Temp: " + String(data.temperature, 1) + "°C");
  Serial.println("Humidity: " + String(data.humidity, 1) + "%");
  Serial.println("---");
  
  lcd.setCursor(0, 0);
  lcd.print("  Temp: " + String(data.temperature, 1) + "\xDF" + "C  ");
  lcd.setCursor(0, 1);
  lcd.print(" Humidity: " + String(data.humidity, 1) + "% ");
  lcd.print("Wokwi Online IoT");


  if (data.temperature > 24.0) {
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(server);
      http.addHeader("Content-Type", "application/json");

      String payload = "{\"temperature\":" + String(data.temperature, 2) + "}";

      int httpResponseCode = http.POST(payload);
      if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
      } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    } else {
      Serial.println("Wi-Fi Disconnected!");
    }
  }

  delay(5000); 
}