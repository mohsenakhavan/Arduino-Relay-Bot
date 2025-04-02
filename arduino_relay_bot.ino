/*
 * Arduino Relay Bot
 * 
 * Controls 8 relays based on serial commands from a Telegram bot
 * Author: Mohsen Akhavan
 */

// Arduino standard library is implicitly included
#include <Arduino.h>

// Define relay pins (connect to relay module IN1-IN8)
const int relayPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
const int numRelays = 8;

// Variables to track relay states (LOW = ON, HIGH = OFF with most relay modules)
int relayStates[8] = {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH};

// Mode definitions
enum Mode {
  NORMAL,
  ALL_ON,
  ALL_OFF,
  ALTERNATING,
  SEQUENTIAL
};

Mode currentMode = NORMAL;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize relay pins as outputs and set initial state (OFF)
  for (int i = 0; i < numRelays; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], relayStates[i]);
  }
  
  Serial.println("Arduino Relay Bot initialized");
}

void loop() {
  // Check for serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    processCommand(command);
  }
  
  // Process current mode
  handleMode();
  
  delay(100); // Short delay for stability
}

void processCommand(String command) {
  // Commands format:
  // RELAY:n:STATE - Toggle relay n (1-8) to state (0=OFF, 1=ON)
  // MODE:m - Set mode m (0=Normal, 1=All ON, 2=All OFF, 3=Alternating, 4=Sequential)
  
  if (command.startsWith("RELAY:")) {
    // Extract relay number and desired state
    int firstColon = command.indexOf(':');
    int secondColon = command.indexOf(':', firstColon + 1);
    
    if (firstColon != -1 && secondColon != -1) {
      int relayNum = command.substring(firstColon + 1, secondColon).toInt();
      int relayState = command.substring(secondColon + 1).toInt();
      
      // Validate relay number (1-8 in command, 0-7 in array)
      if (relayNum >= 1 && relayNum <= numRelays) {
        setRelay(relayNum - 1, relayState);
        Serial.print("Relay ");
        Serial.print(relayNum);
        Serial.print(" set to ");
        Serial.println(relayState == 0 ? "OFF" : "ON");
      }
    }
  }
  else if (command.startsWith("MODE:")) {
    int modeVal = command.substring(5).toInt();
    setMode(modeVal);
    Serial.print("Mode set to ");
    Serial.println(modeVal);
  }
}

void setRelay(int relay, int state) {
  // Set relay state (0 = OFF, 1 = ON)
  // Note: Most relay modules are active LOW, so we invert the logic
  relayStates[relay] = (state == 0) ? HIGH : LOW;
  digitalWrite(relayPins[relay], relayStates[relay]);
}

void setMode(int mode) {
  switch (mode) {
    case 0:
      currentMode = NORMAL;
      break;
    case 1:
      currentMode = ALL_ON;
      allRelaysOn();
      break;
    case 2:
      currentMode = ALL_OFF;
      allRelaysOff();
      break;
    case 3:
      currentMode = ALTERNATING;
      break;
    case 4:
      currentMode = SEQUENTIAL;
      break;
    default:
      currentMode = NORMAL;
  }
}

void handleMode() {
  static unsigned long lastModeUpdate = 0;
  static int sequentialPosition = 0;
  static bool alternateState = true;
  
  // Only process special modes after intervals
  if (millis() - lastModeUpdate < 500) {
    return;
  }
  
  lastModeUpdate = millis();
  
  switch (currentMode) {
    case NORMAL:
      // Normal mode - do nothing special, just maintain current states
      break;
      
    case ALL_ON:
      // All relays ON - already handled in setMode
      break;
      
    case ALL_OFF:
      // All relays OFF - already handled in setMode
      break;
      
    case ALTERNATING:
      // Alternate relays (odd ON, even OFF, then reverse)
      for (int i = 0; i < numRelays; i++) {
        if (i % 2 == (alternateState ? 0 : 1)) {
          setRelay(i, 1); // ON
        } else {
          setRelay(i, 0); // OFF
        }
      }
      
      alternateState = !alternateState;
      break;
      
    case SEQUENTIAL:
      // Sequential pattern (one relay ON at a time)
      for (int i = 0; i < numRelays; i++) {
        setRelay(i, (i == sequentialPosition) ? 1 : 0);
      }
      
      sequentialPosition = (sequentialPosition + 1) % numRelays;
      break;
  }
}

void allRelaysOn() {
  for (int i = 0; i < numRelays; i++) {
    setRelay(i, 1);
  }
}

void allRelaysOff() {
  for (int i = 0; i < numRelays; i++) {
    setRelay(i, 0);
  }
} 