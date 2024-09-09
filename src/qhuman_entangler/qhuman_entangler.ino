int voltageSensorPin = A7;
int voltageSensorValue = 0;

const int initialVoltageEstimation = 500; // 1024 is about 5V

int delayMs = 60;
const int numSamples = 400;
int voltageSamples[numSamples]; // using it as cyclic array
int sampleIndex = 0;
const int logFreqMs = 2000; // log every 2 seconds

const int outputPin = 13;
bool updateLongMedian = true;
int longMedianVoltage = 0;

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
    Serial.println("Voltage is 0 - skipping measurement");
    digitalWrite(outputPin, LOW);
    delay(delayMs);
    return;
  }

  collectSample(voltageSensorValue);
  logSamples(logFreqMs);

  if (updateLongMedian)
  {
    // in practice the long median will be updated with the 'bad' samples on first touch is lost TODO find other tactic to keep the reference
    longMedianVoltage = calcMedian(numSamples);
  }
  int meduiumMedianVoltage = calcMedian(20);
  int referenceVoltage = max(longMedianVoltage, meduiumMedianVoltage); // the meduin used for faster recovery
  int shortAverageVoltage = calcMovingAverage(5);

  print("Reference: %d (long=%d, meduim=%d), short average: %d", referenceVoltage, longMedianVoltage, meduiumMedianVoltage, shortAverageVoltage);

  if (shortAverageVoltage < referenceVoltage * 0.76)
  {
    Serial.println("Voltage drop detected");
    digitalWrite(outputPin, HIGH);
    updateLongMedian = false;
  }
  if (shortAverageVoltage > referenceVoltage * 0.8)
  {
    digitalWrite(outputPin, LOW);
    updateLongMedian = true;
  }

  // Serial.print("Output pin state ");
  // Serial.println(digitalRead(outputPin) == HIGH ? "HIGH" : "LOW");
  delay(delayMs); // Dynamic delay
}

int calcMovingAverage(int nLastSamples)
{
  int sum = 0;
  int startIndex = (sampleIndex - nLastSamples + numSamples) % numSamples;
  for (int i = 0; i < nLastSamples; i++)
  {
    sum += voltageSamples[(startIndex + i) % numSamples];
  }
  return sum / nLastSamples;
}

int calcMedian(int nLastSamples)
{
  int sortedSamples[nLastSamples];
  int startIndex = (sampleIndex - nLastSamples + numSamples) % numSamples;
  for (int i = 0; i < nLastSamples; i++)
  {
    sortedSamples[i] = voltageSamples[(startIndex + i) % numSamples];
  }
  sort(sortedSamples, nLastSamples);
  int median = sortedSamples[nLastSamples / 2];
  return median;
}

void sort(int *array, int size)
{
  for (int i = 0; i < size - 1; i++)
  {
    for (int j = 0; j < size - i - 1; j++)
    {
      if (array[j] > array[j + 1])
      {
        int temp = array[j];
        array[j] = array[j + 1];
        array[j + 1] = temp;
      }
    }
  }
}

void collectSample(int voltageSensorValue)
{
  voltageSamples[sampleIndex] = voltageSensorValue;
  sampleIndex = (sampleIndex + 1) % numSamples;
}

void logSamples(int logFreqMs)
{
  if (sampleIndex * delayMs % logFreqMs == 0)
  {
    int start = (sampleIndex - logFreqMs / delayMs + numSamples) % numSamples;
    print("Samples (%d - %d):", start, sampleIndex);
    for (int i = start; i < sampleIndex; i++)
    {
      Serial.print(voltageSamples[i]);
      Serial.print(" ");
    }
    Serial.println();
  }
}

void print(const char *format, ...)
{
  char buffer[128];
  va_list args;
  va_start(args, format);
  vsnprintf(buffer, sizeof(buffer), format, args);
  va_end(args);
  Serial.println(buffer);
}