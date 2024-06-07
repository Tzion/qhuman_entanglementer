int voltageSensorPin = A7;
int voltageSensorValue = 0;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  voltageSensorValue = analogRead(voltageSensorPin);
  Serial.print("Voltage measured: ");
  Serial.println(voltageSensorValue);
  Serial.print("Pin A6: ");
  Serial.println(analogRead(A6));
  Serial.print("Pin A5: ");
  Serial.println(analogRead(A5));
  Serial.print("Pin A4: ");
  Serial.println(analogRead(A4));
  Serial.print("Pin A3: ");
  Serial.println(analogRead(A3));
  Serial.print("Pin A2: ");
  Serial.println(analogRead(A2));
  Serial.print("Pin A1: ");
  Serial.println(analogRead(A1));
  delay(1000);
}