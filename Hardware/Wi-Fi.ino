#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <ArduinoJson.h>


const char *ssid = "CSD";
const char *password = "DS1e@CSD78";


const char *websocket_host = "172.25.25.112";
const int websocket_port = 5000;
const char *websocket_path = "/ws";

WebSocketsClient webSocket;
String serialBuffer = "";

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length) {
  switch (type) {
    case WStype_CONNECTED:
      Serial.println("[WSc] WebSocket Connected! ---->");
      break;
    case WStype_DISCONNECTED:
      Serial.println("[WSc] WebSocket Disconnected!");
      break;
    case WStype_TEXT:
      Serial.printf("[WSc] Received from server: %s\n", payload);
      break;
  }
}


String getValueFromString(String data, char separator, int index) {
    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length() - 1;
    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i + 1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}


void setup() {
  Serial.begin(9600);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Wi-Fi connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  webSocket.begin(websocket_host, websocket_port, websocket_path);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);
}

void loop() {
  webSocket.loop();

  if (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      if (serialBuffer.startsWith("DATA:")) {
        String sensorValues = serialBuffer.substring(5);
s.
        StaticJsonDocument<128> jsonDoc;


        float moisture = getValueFromString(sensorValues, ',', 0).toFloat();
        float temp = getValueFromString(sensorValues, ',', 1).toFloat();
        float humidity = getValueFromString(sensorValues, ',', 2).toFloat();


        jsonDoc["Soil_Moisture"] = moisture;
        jsonDoc["Soil_Temperature"] = temp;
        jsonDoc["Humidity"] = humidity;


        String output;
        serializeJson(jsonDoc, output);

        webSocket.sendTXT(output);
      }
      serialBuffer = "";
    } else if (c != '\r') {
      serialBuffer += c;
    }
  }
}