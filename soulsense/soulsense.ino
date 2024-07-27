#include <PulseSensorPlayground.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Arduino.h>

const int PULSE_INPUT = 34;
const int PULSE_BLINK = 13;
const int PULSE_FADE = 5;   // Pin for the onboard LED
const int THRESHOLD = 685;  // Adjust this value to tune the sensor

PulseSensorPlayground pulseSensor;

const char* ssid = "duFIFA";
const char* password = "Fahri8013";
const char* serverAPI = "http://192.168.1.8:5001/api/sensor/store_data";

bool sendPulseSignal = false;

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.print("Attempting to connect to ");
  Serial.print(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  analogReadResolution(10);

  // Configure pulse sensor
  pulseSensor.analogInput(PULSE_INPUT);
  pulseSensor.blinkOnPulse(PULSE_BLINK);
  pulseSensor.fadeOnPulse(PULSE_FADE);
  pulseSensor.setSerial(Serial);
  pulseSensor.setThreshold(THRESHOLD);

  /*  Now that everything is ready, start reading the PulseSensor signal. */
  if (!pulseSensor.begin()) {
    while (1) {
      /*  If the pulseSensor object fails, flash the led  */
      digitalWrite(PULSE_BLINK, LOW);
      delay(500);
      digitalWrite(PULSE_BLINK, HIGH);
      delay(500);
    }
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverAPI);

    if (sendPulseSignal) {
      delay(200);
      Serial.println(pulseSensor.getLatestSample());
    }
    // Get the BPM value
    int myBPM = 0;

    // If a beat is detected
    if (pulseSensor.sawStartOfBeat()) {
      myBPM = pulseSensor.getBeatsPerMinute();

      if (myBPM < 200) {

        http.addHeader("Content-Type", "application/json");

        Serial.print("BPM: ");
        Serial.println(myBPM);
        int stressLevel = calculateStressLevel(myBPM);
        Serial.print("Stress Level: ");
        Serial.println(stressLevel);

        StaticJsonDocument<200> doc;
        doc["value"] = myBPM;
        doc["level"] = stressLevel;

        String requestBody;
        serializeJson(doc, requestBody);

        int httpResponseCode = http.POST(requestBody);

        if (httpResponseCode > 0) {
          String response = http.getString();
          Serial.println(httpResponseCode);
          Serial.println(response);
        } else {
          Serial.print("Error on sending POST: ");
          Serial.println(httpResponseCode);
        }

        http.end();
      }
    }
  } else {
    Serial.println("Error in WiFi connection");
  }
  delay(200);
  // serialCheck();
}

void serialCheck(){
  if(Serial.available() > 0){
    char inChar = Serial.read();
    switch(inChar){
      case 'b':
        sendPulseSignal = true;
        break;
      case 'x':
        sendPulseSignal = false;
        break;
      default:
        break;
    }
  }
}

int calculateStressLevel(int bpm) {
  // Simple stress calculation based on BPM thresholds
  if (bpm < 60) {
    return 1;  // Low stress
  } else if (bpm >= 60 && bpm <= 100) {
    return 2;  // Moderate stress
  } else {
    return 3;  // High stress
  }
}
