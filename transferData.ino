#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Create an instance of the display
Adafruit_SSD1306 display(128, 64, &Wire, -1);

int wordCount = 0;
bool inWord = false;
String text = "";

void setup() {
  // Initialize the display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  Serial.begin(9600);
  // Additional display settings if needed
}
void loop() {
  
  if (Serial.available())
  {
    display.clearDisplay();    
    
    text = Serial.readString();
    countWords();
    
    // Set text properties
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);

    // Set the text position
    display.setCursor(0, 0);
    // Print the text
  
    display.println(text);
    display.display();
  // Display the text
  }
 delay(250*wordCount);
 display.clearDisplay();
 display.display();
}

void countWords() {
  for (size_t i = 0; i < text.length(); i++) {
    if (isAlpha(text.charAt(i))) { // Check if character is alphabetic
      if (!inWord) {
        inWord = true;
        wordCount++;
      }
    } else {
      inWord = false;
    }
  }
}
