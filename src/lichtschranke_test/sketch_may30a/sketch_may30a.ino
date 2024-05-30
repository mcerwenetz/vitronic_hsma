
int diodePin = 2;
int status_photodiode_n_0 = 0;
int status_photodiode_n_1 = 0;

// Variables 
long starttime_0;
long stoptime_0;
long difftime_0 = 0;

int status_timemeasurement = 0;
int change = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(diodePin, INPUT);
  Serial.begin(9600);
}

void loop() {
  status_photodiode_n_0 = digitalRead(diodePin);
  //check if light is on diode
  if(status_photodiode_n_0 == 1){
    //if switch is 0 set starttime_0
    if(status_timemeasurement == 0){
      starttime_0 = millis();
      status_timemeasurement = 1;
    }
  }
  //light is off on diode
  else{
    if(status_timemeasurement == 1){
      stoptime_0 = millis();
      status_timemeasurement = 0;
      change = 1;
    }
  }
  if(change == 1){
    difftime_0 = stoptime_0 - starttime_0;
    if (difftime_0 > 5) {
      Serial.print("Unterbrechung Laserschranke: ");
      Serial.print(difftime_0);
      Serial.print(" ms");
      Serial.println();
    }
    change = 0;  
  }
  delay(0.1);
}
