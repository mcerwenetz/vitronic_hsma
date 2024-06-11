// Pin Out
int Diode0Pin = 2;
int Diode1Pin = 3;

// Interrupted Laser digital read
bool status_Laser0;

// Time measurement
int status_timemeasurment = 0;
int newtime = 0;
long starttime;
long stoptime;
long difftime = 0;

// Height detection
bool height0 = 0;
bool height1 = 0;

void setup() {
  pinMode(Diode0Pin, INPUT);
  pinMode(Diode1Pin, INPUT);
  Serial.begin(115200);
}

void loop() {
  status_Laser0 = debounceSwitch(Diode0Pin);
  // detect interruption of laser
  if (status_Laser0 == 1)
  {
    if (status_timemeasurment == 0)
      starttime = millis();
      if (status_timemeasurment == 0)
      {
        Serial.println("interrupted light barrier");
      }
      status_timemeasurment = 1;
      delay(0.1);
      heightDetection();
  }
  // laser is uninterrupted again
  else
  {
    if(status_timemeasurment == 1)
    {
      status_timemeasurment = 0;
      stoptime = millis();
      newtime = 1;
    }
  }

  // new timemeaserent return value
  if (newtime == 1)
  {
    newtime = 0;
    difftime = stoptime - starttime;
    if (difftime > 5) 
    {
      Serial.print(difftime);
      Serial.print(" ms, heigth: ");
      Serial.print(height1);
      Serial.print(height0);
      Serial.println();
      height0 = 0;
      height1 = 0;
    }
  }
  
  delay(0.1);
}

bool debounceSwitch(int Pin) {
    bool currentState = digitalRead(Pin);
    delay(5);  // Warten für die Entprellungszeit
    bool newState = digitalRead(Pin);

    if (currentState == newState) {
        return newState;
    } else {
        return debounceSwitch(Pin);  // Wiederhole, wenn nicht stabil
    }
}

void heightDetection() {
  if(debounceSwitch(Diode0Pin) == 1) {
      height0 = 1;
  }
  if(debounceSwitch(Diode1Pin) == 1) {
      height1 = 1;
  }
}
