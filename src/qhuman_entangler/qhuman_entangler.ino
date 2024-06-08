int voltageSensorPin = A7;
int voltageSensorValue = 0;

const int numSamples = 46;
const int initialVoltageEstimation = 533; // guessig the initial voltage (~2.4V)
int voltageSamples[numSamples];  // using it as cyclic array, initialized with 0
int sampleIndex = 0;
const int outputPin = 9;
bool pauseSampling = false;

void setup()
{
  Serial.begin(9600);
  digitalWrite(outputPin, LOW);
  // initialize the samlpes with the estimated voltage to help reaching steady state faster
  for (int i=0; i<numSamples; i++) {
    voltageSamples[i] = initialVoltageEstimation;
  }
}

void loop()
{
  voltageSensorValue = analogRead(voltageSensorPin);
  Serial.print("Voltage measured of pin A7:");
  Serial.println(voltageSensorValue);

// when there's contact (low voltage) we want to keep the average value as a reference point
if (!pauseSampling) {
  voltageSamples[sampleIndex] = voltageSensorValue;
  sampleIndex = (sampleIndex + 1) % numSamples;
}

  int sum = 0;
  for (int i = 0; i < numSamples; i++)
  {
    sum += voltageSamples[i];
  }
  int samplesAverage = sum / numSamples;
  Serial.print("Average voltage: ");
  Serial.println(samplesAverage);

  if (voltageSensorValue < samplesAverage * .83) {
    Serial.println("Voltage drop detected");
    digitalWrite(outputPin, HIGH);
    pauseSampling = true;
  }
  if (voltageSensorValue > samplesAverage * .92) {
    digitalWrite(outputPin, LOW);
    pauseSampling = false;
  }
  Serial.print("Output pin state: ");
  Serial.println(digitalRead(outputPin) == HIGH ? "HIGH" : "LOW");
  delay(500);
}