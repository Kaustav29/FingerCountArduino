const int ledPin = 7; // Assuming LED is connected to pin 7

void setup() {
    Serial.begin(9600);
    pinMode(ledPin, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        int upCount = Serial.parseInt(); // Read the value from the serial port
        for (int i = 0; i < upCount; i++) {
            digitalWrite(ledPin, HIGH); // Turn on the LED
            delay(500); // Wait for 500ms
            digitalWrite(ledPin, LOW); // Turn off the LED
            delay(500); // Wait for 500ms
        }
    }
}

