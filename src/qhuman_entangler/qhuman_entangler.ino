int voltageSensorPin = A7;
int voltageSensorValue = 0;

const int initialVoltageEstimation = 500; // 1024 is about 5V

int delayMs = 50;
const int numSamples = 400;
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
    Serial.println("Voltage is 0 - wires may be disconnected - skipping measurement");
    digitalWrite(outputPin, LOW);
    delay(delayMs);
    return;
  }

  collectSample(voltageSensorValue);
  logSamples(logFreqMs);

  int LongMedianVoltage = calcMedian(numSamples);
  int shortAverageVoltage = calcMovingAverage(5);

  print("Long Median voltage: %d short average: %d", LongMedianVoltage, shortAverageVoltage);

  if (shortAverageVoltage < LongMedianVoltage * 0.72)
  {
    Serial.println("Voltage drop detected");
    digitalWrite(outputPin, HIGH);
    // pauseSampling = true;
  }
  if (shortAverageVoltage > LongMedianVoltage * 0.8)
  {
    digitalWrite(outputPin, LOW);
    pauseSampling = false;
  }

  // Serial.print("Output pin state ");
  // Serial.println(digitalRead(outputPin) == HIGH ? "HIGH" : "LOW");
  delay(delayMs); // Dynamic delay
}

int calcMovingAverage(int nLastSamples) {
  int sum = 0;
  int startIndex = (sampleIndex - nLastSamples + numSamples) % numSamples;
  for (int i = 0; i < nLastSamples; i++) {
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