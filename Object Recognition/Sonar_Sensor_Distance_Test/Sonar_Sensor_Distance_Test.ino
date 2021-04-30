#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
#define servoPin 4

#include <Servo.h>
Servo servo;
int pos = 0;

// defines variables
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement

float farTime = 200 * 2 / 0.034; //Timeout based on farthest distance to account for

double getDistance() {
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH, farTime);
  
  // Calculating the distance
  distance = (duration * 0.034) / 2; // Speed of sound wave divided by 2 (go and back)

  return distance;
}

void printDist(int dist) {
  Serial.print("Distance: ");
  Serial.print(dist);
  Serial.println(" cm");
}


void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  servo.attach(servoPin);
}
void loop() {
//  // Clears the trigPin condition
//  digitalWrite(trigPin, LOW);
//  delayMicroseconds(2);
//  
//  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
//  digitalWrite(trigPin, HIGH);
//  delayMicroseconds(10);
//  digitalWrite(trigPin, LOW);
//  
//  // Reads the echoPin, returns the sound wave travel time in microseconds
//  duration = pulseIn(echoPin, HIGH, farTime);
//  
//  // Calculating the distance
//  distance = (duration * 0.034) / 2; // Speed of sound wave divided by 2 (go and back)

  distance = getDistance();
  
  // Displays the distance on the Serial Monitor
//  Serial.print("Distance: ");
//  Serial.print(distance);
//  Serial.println(" cm");
  printDist(distance);
  delay(100);
  
  if (distance <= 30 && distance > 0) {
    bool obsOnLeft = false;
    bool obsOnRight = false;
    
    // check left side
    for (pos = 90; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      servo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }

    Serial.println("Checking left");
    for (int i = 0; i < 10; i += 1) {
      double dist = getDistance();
      printDist(dist);
      delay(50);

      if (dist <= 30 && distance > 0) {
        obsOnLeft = true;
      }
    }
    
    delay(100);

    for (pos = 180; pos >= 90; pos -= 1) { // goes from 180 degrees to 0 degrees
      servo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(15);                       // waits 15ms for the servo to reach the position
    }

    

    //check right side
    for (pos = 90; pos >= 0; pos -= 1) {
      servo.write(pos);
      delay(15);
    }
    
    Serial.println("Checking right");
    for (int i = 0; i < 10; i += 1) {
      double dist = getDistance();
      printDist(dist);
      delay(50);

      if (dist <= 30 && distance > 0) {
        obsOnRight = true;
      }
    }

    delay(100);

    for (pos = 0; pos <= 90; pos += 1) {
      servo.write(pos);
      delay(15);
    }


    Serial.print("obsOnLeft ");
    Serial.println(obsOnLeft);
    Serial.print("obsOnRight ");
    Serial.println(obsOnRight);
    delay(2000);

    if (!obsOnRight) {
      Serial.println("going right");
      
      for (pos = 90; pos >= 0; pos -= 1) {
        servo.write(pos);
        delay(15);
      }

      delay(2000);

      for (pos = 0; pos <= 90; pos += 1) {
        servo.write(pos);
        delay(15);
      }
    }
    else if (!obsOnLeft) {
      Serial.println("going left");
      
      for (pos = 90; pos <= 180; pos += 1) {
        servo.write(pos);
        delay(15);
      }

      delay(2000);

      for (pos = 180; pos >= 90; pos -= 1) {
        servo.write(pos);
        delay(15);
      }
    }
  }
}
