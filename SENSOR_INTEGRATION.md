# Sensor Hardware Integration Guide

This guide explains how to integrate IoT sensors with the Environmental Health Platform.

## Supported Sensors

### Air Quality Sensors
- **PMS5003 / SPS30**: PM2.5 and PM10 particulate matter
- **SCD41**: CO2 concentration
- **BME680 / ENS160**: VOC (Volatile Organic Compounds), Temperature, Humidity
- **MiCS-4514** (optional): NO2 concentration

### Microcontroller
- **ESP32**: WiFi-enabled microcontroller for data transmission

## Hardware Setup

### Basic Configuration

1. **Connect Sensors to ESP32**
   - PMS5003: TX/RX pins
   - SCD41: I2C (SDA/SCL)
   - BME680: I2C (SDA/SCL)

2. **Power Supply**
   - 5V USB power adapter
   - Ensure stable power for accurate readings

### Wiring Diagram

```
ESP32 Pinout:
- GPIO 21: I2C SDA (BME680, SCD41)
- GPIO 22: I2C SCL (BME680, SCD41)
- GPIO 16: UART RX (PMS5003)
- GPIO 17: UART TX (PMS5003)
```

## Firmware

### Example ESP32 Firmware (Arduino/PlatformIO)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include "PMS.h"
#include "Adafruit_SCD30.h"
#include "Adafruit_BME680.h"

// Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* apiUrl = "http://your-api-url.com/api/indoor/readings";
const char* authToken = "YOUR_JWT_TOKEN";
const char* deviceId = "YOUR_DEVICE_ID";

// Sensor objects
PMS pms(Serial2);
Adafruit_SCD30 scd30;
Adafruit_BME680 bme;

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600);  // PMS5003
  Wire.begin();
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  
  // Initialize sensors
  if (!scd30.begin()) {
    Serial.println("Failed to find SCD30 sensor");
  }
  
  if (!bme.begin()) {
    Serial.println("Failed to find BME680 sensor");
  }
  
  // Configure BME680
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);
}

void loop() {
  // Read PMS5003
  PMS::DATA pmsData;
  float pm25 = 0, pm10 = 0;
  if (pms.readUntil(pmsData)) {
    pm25 = pmsData.PM_AE_UG_2_5;
    pm10 = pmsData.PM_AE_UG_10_0;
  }
  
  // Read SCD30
  float co2 = 0;
  if (scd30.dataReady()) {
    if (scd30.read()) {
      co2 = scd30.CO2;
    }
  }
  
  // Read BME680
  float temp = 0, humidity = 0;
  int vocIndex = 0;
  if (bme.performReading()) {
    temp = bme.temperature;
    humidity = bme.humidity;
    // VOC index calculation (simplified)
    vocIndex = map(bme.gas_resistance, 0, 100000, 500, 0);
  }
  
  // Send data to API
  sendSensorData(pm25, pm10, co2, vocIndex, temp, humidity);
  
  // Wait 60 seconds before next reading
  delay(60000);
}

void sendSensorData(float pm25, float pm10, float co2, int vocIndex, 
                   float temp, float humidity) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(apiUrl);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", String("Bearer ") + authToken);
    
    // Create JSON payload
    StaticJsonDocument<512> doc;
    doc["device_id"] = deviceId;
    doc["ts"] = getISOTimestamp();
    doc["pm25"] = pm25;
    doc["pm10"] = pm10;
    doc["co2"] = co2;
    doc["voc_index"] = vocIndex;
    doc["temp"] = temp;
    doc["humidity"] = humidity;
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error sending data: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  }
}

String getISOTimestamp() {
  // Get time from NTP server (simplified)
  // In production, use proper NTP time sync
  time_t now;
  struct tm timeinfo;
  time(&now);
  gmtime_r(&now, &timeinfo);
  
  char buffer[30];
  strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
  return String(buffer);
}
```

## Data Publishing Protocol

### JSON Payload Format

```json
{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts": "2025-09-01T18:30:00Z",
  "pm25": 12.4,
  "pm10": 22.1,
  "co2": 945,
  "voc_index": 112,
  "temp": 27.1,
  "humidity": 54.0
}
```

### HTTP POST Request

```bash
POST /api/indoor/readings HTTP/1.1
Host: your-api-url.com
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts": "2025-09-01T18:30:00Z",
  "pm25": 12.4,
  "pm10": 22.1,
  "co2": 945,
  "voc_index": 112,
  "temp": 27.1,
  "humidity": 54.0
}
```

## Reading Frequency

- **Recommended**: 60 seconds
- **Minimum**: 30 seconds
- **Maximum**: 5 minutes

More frequent readings consume more power and bandwidth but provide better real-time monitoring.

## Calibration

### Initial Calibration
1. Place sensor in known good air quality environment
2. Let it stabilize for 24 hours
3. Record baseline readings
4. Apply calibration offset if needed

### Regular Maintenance
- Clean sensors monthly
- Recalibrate quarterly
- Replace sensors per manufacturer guidelines

## Data Quality

### Averaging Readings
Average multiple readings over 5 minutes to reduce noise:

```cpp
float averagePM25(PMS &pms, int samples = 5) {
  float sum = 0;
  int validReadings = 0;
  
  for (int i = 0; i < samples; i++) {
    PMS::DATA data;
    if (pms.readUntil(data)) {
      sum += data.PM_AE_UG_2_5;
      validReadings++;
    }
    delay(1000);
  }
  
  return validReadings > 0 ? sum / validReadings : 0;
}
```

### Error Handling
- Retry failed transmissions up to 3 times
- Store readings locally if network unavailable
- Send buffered readings when connection restored

## Power Management

### Battery Operation
```cpp
// Deep sleep between readings
void enterDeepSleep(int minutes) {
  esp_sleep_enable_timer_wakeup(minutes * 60 * 1000000ULL);
  esp_deep_sleep_start();
}
```

### Power Consumption
- Active mode: ~80mA
- Deep sleep: ~10µA
- Estimated battery life: 
  - 2000mAh battery with 60s readings: ~24 hours
  - With 5-minute intervals: ~7 days

## Troubleshooting

### Common Issues

1. **Sensor not detected**
   - Check I2C connections
   - Verify I2C address with scanner
   - Ensure proper power supply

2. **Erratic readings**
   - Check for loose connections
   - Verify sensor is not obstructed
   - Allow warm-up time (5-10 minutes)

3. **Network errors**
   - Verify WiFi credentials
   - Check API endpoint URL
   - Ensure JWT token is valid

4. **High CO2 readings**
   - Ensure proper ventilation
   - Calibrate in fresh air
   - Check sensor placement

## Best Practices

1. **Placement**
   - Height: 1-2 meters above floor
   - Away from direct airflow (windows, vents)
   - Not in direct sunlight
   - Away from heat sources

2. **Enclosure**
   - Ventilated case for air circulation
   - Protect from dust and moisture
   - Allow sensor warmup

3. **Security**
   - Store JWT tokens securely
   - Use HTTPS for API calls
   - Implement OTA updates carefully

## Alternative Protocols

### MQTT (Future Phase)

```cpp
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  // ... WiFi setup ...
  client.setServer("mqtt-broker.com", 1883);
}

void publishReading() {
  if (client.connect("ESP32Sensor", "username", "password")) {
    StaticJsonDocument<512> doc;
    // ... populate doc ...
    
    char buffer[512];
    serializeJson(doc, buffer);
    client.publish("sensors/readings", buffer);
  }
}
```

## Resources

- [ESP32 Documentation](https://docs.espressif.com/)
- [PMS5003 Datasheet](https://www.plantower.com/)
- [SCD41 Documentation](https://www.sensirion.com/)
- [BME680 Documentation](https://www.bosch-sensortec.com/)

## Support

For hardware integration questions, open an issue on GitHub with the "hardware" label.
