
int diodePin = 2;
int val = 0;

long starttime;
long stoptime;
long longest = 0;
long diff = 0;

int swtch = 0;
int change = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(diodePin, INPUT);
  Serial.begin(9600);
}

void loop() {

  val = digitalRead(diodePin);
  //check if light is on diode
  if(val == 0){
    //if switch is 0 set starttime
    if(swtch == 0){
      starttime = millis();
      swtch = 1;
    }
  }
  //light is off on diode
  else{
    if(swtch == 1){
      stoptime = millis();
      swtch = 0;
      change = 1;
    }
  }
  if(change == 1){
    diff = stoptime - starttime;
    Serial.println("new diff");
    Serial.print(diff);
    //find max
    if(diff > longest){
      longest = diff;
      Serial.println("new longest");
      Serial.print(longest);
    }
    change = 0;  
  }
  delay(0.1);
}
