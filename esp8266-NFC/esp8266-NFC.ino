#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <ESP8266WiFi.h>

// WiFi credentials
const char* ssid = "HaggagNet";
const char* password = "19991996";

// Server details
const char* server_ip = "192.168.1.101";  // Laptop/server's IP address
const int server_port = 2020;             // Choose an available port

WiFiClient client;

// Pin configuration for I2C communication with PN532
#define SDA_PIN D1
#define SCL_PIN D2

// Create instances of PN532_I2C and PN532
PN532_I2C pn532_i2c(Wire);
PN532 nfc(pn532_i2c);

void setup(void) {
  Serial.begin(115200);

  // Initialize PN532 and serial communication
  nfc.begin();
  Serial.println("\nConnecting to WiFi...");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
  Serial.println("Connected to WiFi");

  Serial.println("Connecting to server...");

  // Connect to the server
  while (!client.connect(server_ip, server_port)) {
    Serial.println("Connecting to server");
  }
  Serial.println("Connected to server...");

  // Check PN532 board firmware version
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.println("Didn't find PN53x board");
    while (!versiondata) {
      versiondata = nfc.getFirmwareVersion();
      delay(1000);
    }
  }

  // Configure PN532
  nfc.SAMConfig();
  Serial.println("Waiting for an NFC card...");
}

void loop(void) {
  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };
  uint8_t uidLength;

  // Attempt to read an NFC card
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);
  String ids;

  if (success) {
    // Reconnect to the server (if not already connected)
    if (client.connect(server_ip, server_port)) {
      Serial.println("Connected to server");
    } else {
      Serial.println("Connection to server failed");
    }

    Serial.println("Found an NFC card!");

    Serial.print("UID Length: ");
    Serial.print(uidLength, DEC);
    Serial.println(" bytes");
    Serial.print("UID Value: ");
    
    // Print and store UID in ids string
    for (uint8_t i=0; i < uidLength; i++) {
      Serial.print(uid[i], HEX);
      ids += String(uid[i], HEX);
    }
    
    Serial.println("");
    Serial.println("");

    // Send UID to the server if connected
    if (client.connected()) {
      client.println(ids);
    }

    delay(1000);  // Adjust delay as needed

    ids = "";  // Clear 'ids' for the next NFC card
  }
}
