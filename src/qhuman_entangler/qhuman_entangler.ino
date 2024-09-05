int voltageSensorPin = A7;
int voltageSensorValue = 0;

const int initialVoltageEstimation = 1000; // guessig the initial voltage (~5V)
const int sampleFrequencyHz = 100;
const int desiredActivationTime = 300; // in ms, this is actually the maximal time and the actual time will be half of it

int delayMs = 50;
const int numSamples = 600;
int voltageSamples[numSamples]; // using it as cyclic array
int sampleIndex = 0;
const int logFreqMs = 2000; // log every 2 seconds

const int outputPin = 13;
bool pauseSampling = false;

void setup()
{
  Serial.begin(9600);
  digitalWrite(outputPin, LOW);
  // initialize the samlpes with the estimated voltage to help reaching steady state faster
  // initializeSamples(initialVoltageEstimation);
}

void initializeSamples(int voltage)
{
  for (int i = 0; i < numSamples; i++)
  {
    voltageSamples[i] = initialVoltageEstimation;
  }
}

void loop()
{
  voltageSensorValue = analogRead(voltageSensorPin);

  if (voltageSensorValue == 0)
  {
    // Serial.println("Voltage is 0 - wires may be disconnected - skipping measurement");
    digitalWrite(outputPin, LOW);
    delay(delayMs); 
    return;
  }

  collectSample(voltageSensorValue);
  logSamples(logFreqMs);

  // Sort the samples
  int sortedSamples[numSamples];
  memcpy(sortedSamples, voltageSamples, sizeof(voltageSamples));
  // std::sort(sortedSamples, sortedSamples + numSamples);

  // Use the middle sample as the filtered value (median)
  int filteredValue = sortedSamples[numSamples / 2];

  // Serial.print("Filtered voltage (median): ");
  // Serial.println(filteredValue);

  if (voltageSensorValue < filteredValue * 0.8)
  {
    // Serial.println("Voltage drop detected");
    digitalWrite(outputPin, HIGH);
    pauseSampling = true;
  }
  if (voltageSensorValue > filteredValue * 0.4)
  {
    digitalWrite(outputPin, LOW);
    pauseSampling = false;
  }

  // Serial.print("Output pin state: ");
  // Serial.println(digitalRead(outputPin) == HIGH ? "HIGH" : "LOW");
  delay(delayMs); // Dynamic delay
}

void collectSample(int voltageSensorValue)
{
  // when there's contact (low voltage), collect samples
  if (!pauseSampling)
  {
    voltageSamples[sampleIndex] = voltageSensorValue;
    sampleIndex = (sampleIndex + 1) % numSamples;
  }
}

void logSamples(int logFreqMs)
{
  if (sampleIndex * delayMs % logFreqMs == 0)
  {
    int start = (sampleIndex - logFreqMs / delayMs + numSamples ) % numSamples;
    printf("\n");
    Serial.print("Samples (");
    Serial.print(start);
    Serial.print(" - ");
    Serial.print(sampleIndex);
    Serial.println("):");
    for (int i = start; i < sampleIndex; i++)
    {
      Serial.print(voltageSamples[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
}