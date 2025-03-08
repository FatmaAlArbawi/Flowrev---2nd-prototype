#include <Wire.h>  // Include Wire library for I2C communication
#include "MAX30100_PulseOximeter.h"  // Include library for MAX30100 sensor

const int EEG_PIN = A0;  // Define analog pin for EEG sensor
const int TEMP_PIN = A1;  // Define analog pin for temperature sensor
const int MOTOR_PIN = 9;  // Define digital pin for motor control

PulseOximeter pox;  // Create PulseOximeter object

void setup() {
  Serial.begin(115200);  // Initialize serial communication at 115200 baud rate
  pinMode(MOTOR_PIN, OUTPUT);  // Set motor pin as output
  
  if (!pox.begin()) {  // Initialize MAX30100 sensor
    Serial.println("MAX30100 was not found");  // Print error message if sensor not found
    while(1);  // Infinite loop if sensor initialization fails
  }

}

void loop() {
  pox.update();  // Update MAX30100 sensor readings
  
  int eegValue = analogRead(EEG_PIN);  // Read EEG sensor value
  int tempValue = analogRead(TEMP_PIN);  // Read temperature sensor value
  float heartRate = pox.getHeartRate();  // Get heart rate from MAX30100
  float spO2 = pox.getSpO2();  // Get SpO2 from MAX30100
  
  // Send all sensor data to Raspberry Pi
  Serial.print(eegValue);
  Serial.print(",");
  Serial.print(tempValue);
  Serial.print(",");
  Serial.print(heartRate);
  Serial.print(",");
  Serial.println(spO2);
  
  // Check for motor control commands from Raspberry Pi
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read command from serial
    digitalWrite(MOTOR_PIN, command == '1' ? HIGH : LOW);  // Set motor state based on command
  }
  
  delay(10);  // Short delay to avoid flooding the serial port
 
 
}
