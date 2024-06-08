int voltageSensorPin = A7;
int voltageSensorValue = 0;

const int numSamples = 46;
const int initialVoltageEstimation = 533; // guessing the value to help reaching steady state faster
int voltageSamples[numSamples] = {initialVoltageEstimation};  // using it as cyclic array, initialized with 0
int sampleIndex = 0;
const int outputPin = 9;

void setup()
{
  Serial.begin(9600);
  digitalWrite(outputPin, LOW);
}

void loop()
{
  voltageSensorValue = analogRead(voltageSensorPin);
  Serial.print("Voltage measured of pin A7:");
  Serial.println(voltageSensorValue);

  voltageSamples[sampleIndex] = voltageSensorValue;
  sampleIndex = (sampleIndex + 1) % numSamples;

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
  }
  if (voltageSensorValue > samplesAverage * .92) {
    digitalWrite(outputPin, LOW);
  }
  Serial.print("Output pin state: ");
  Serial.println(digitalRead(outputPin) == HIGH ? "HIGH" : "LOW");
  delay(500);
}