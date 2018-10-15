#include <Mouse.h>

const int pinRight = 2;
const int pinLeft = 3;

void setup() {
  pinMode(pinLeft, INPUT);
  pinMode(pinRight, INPUT);
  digitalWrite(pinLeft, HIGH);
  digitalWrite(pinRight, HIGH);
  Mouse.begin();
}

void loop() {
  int leftClick = digitalRead(pinLeft);
  int rightClick = digitalRead(pinRight);
  
  if (leftClick == LOW && !Mouse.isPressed(MOUSE_LEFT)) {
    Mouse.press(MOUSE_LEFT);
  } else if (leftClick == HIGH && Mouse.isPressed(MOUSE_LEFT)) {
    Mouse.release(MOUSE_LEFT);
  }
  
  if (rightClick == LOW && !Mouse.isPressed(MOUSE_RIGHT)) {
    Mouse.press(MOUSE_RIGHT);
  } else if (rightClick == HIGH && Mouse.isPressed(MOUSE_RIGHT)) {
    Mouse.release(MOUSE_RIGHT);
  }
}
