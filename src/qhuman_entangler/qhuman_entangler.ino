#include <algorithm>
int voltageSensorPin = A7;
int voltageSensorValue = 0;

const int initialVoltageEstimation = 1020; // guessig the initial voltage (~2.4V)
const int SampleFrequency = 100; // in Herz
const int DesiredActivationTime = 300; // in ms, this is actually the maximal time and the actual time will be half of it

int DeltaT = int(1000 / SampleFrequency);  // in ms
int numSamples = int(Hz * DesiredActivationTime / 1000);  // number of samples to collect
int voltageSamples[numSamples];  // using it as cyclic array, initialized with 0
int sampleIndex = 0;

const int outputPin = 13;
bool pauseSampling = false;

void setup()
{
  Serial.begin(9600);
  digitalWrite(outputPin, LOW);
  // initialize the samlpes with the estimated voltage to help reaching steady state faster
  // initializeSamples(initialVoltageEstimation);
}

void initializeSamples(int voltage) {
  for (int i=0; i<numSamples; i++) {
    voltageSamples[i] = initialVoltageEstimation;
  }
}

void loop()
{
  voltageSensorValue = analogRead(voltageSensorPin);
  Serial.print("Voltage measured of pin A7:");
  Serial.println(voltageSensorValue);

  if (voltageSensorValue == 0) {
    Serial.println("Voltage is 0 - wires may be disconnected - skipping measurement");
    digitalWrite(outputPin, LOW);
    delay(DeltaT);  // Dynamic delay
    return;
  }

  // when there's contact (low voltage), collect samples
  if (!pauseSampling) {
    voltageSamples[sampleIndex] = voltageSensorValue;
    sampleIndex = (sampleIndex + 1) % numSamples;
  }

  // Sort the samples
  int sortedSamples[numSamples];
  memcpy(sortedSamples, voltageSamples, sizeof(voltageSamples));
  std::sort(sortedSamples, sortedSamples + numSamples);

  // Use the middle sample as the filtered value (median)
  int filteredValue = sortedSamples[numSamples / 2];

  Serial.print("Filtered voltage (median): ");
  Serial.println(filteredValue);

  if (voltageSensorValue < filteredValue * 0.8) {
    Serial.println("Voltage drop detected");
    digitalWrite(outputPin, HIGH);
    pauseSampling = true;
  }
  if (voltageSensorValue > filteredValue * 0.4) {
    digitalWrite(outputPin, LOW);
    pauseSampling = false;
  }

  Serial.print("Output pin state: ");
  Serial.println(digitalRead(outputPin) == HIGH ? "HIGH" : "LOW");
  delay(DeltaT);  // Dynamic delay
}