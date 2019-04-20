//
//#define trigPin 2
//#define echoPin 3
//#define trigPin2 4 
//#define echoPin2 5
const int trigPin = 2;
const int echoPin = 3;
const int trigPin2 = 4;
const int echoPin2 = 5;
 
void setup() {
 Serial.begin (9600); 
 
 pinMode(trigPin, OUTPUT); 
 pinMode(echoPin, INPUT);  
pinMode(trigPin2, OUTPUT);
 pinMode(echoPin2, INPUT);
}

int check_distance(int distance){
   if (distance >= 100000 || distance <= 0){
      return 0;
    }
    return distance;
 }

void loop() {
 long distance1, distance2;
 distance1 = ultra_sonic(trigPin, echoPin);
 distance2 = ultra_sonic(trigPin2, echoPin2);
 
 long total_distance = distance1 + distance2;
 String json = "";
 json = json + "{";
 json = json + "\"Distance\":" + String(total_distance - 3);
 json = json + "}";
 Serial.println(json);
 delay(500);
}

int ultra_sonic(int trigPin, int echoPin){
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2); // waiting for 2 microseconds
  digitalWrite(trigPin, HIGH); // sending the signal to the sonic to trigger it
  delayMicroseconds(10); // keeping the output as HIGH to create the 10 microsecond pulse for triger
 digitalWrite(trigPin, LOW); // setting output back to LOW, now the triger pulse is generated and accordingly
 duration = pulseIn(echoPin, HIGH); // get the calculated duration from the function
 distance = (duration/2) / 29; // considers the speed of sound [(343.2m/s)/10000]
  return distance;
}
