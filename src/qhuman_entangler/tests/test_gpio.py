import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
gpio_pins = list(range(2, 27))  # Read all GPIO pins on Raspberry Pi

def test_read_gpio_pins():
    def handle_gpio_change(pin):
        print(f"GPIO pin {pin} changed")

    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.IN)
        try:
            print(f"adding event detection for pin {pin}")
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=handle_gpio_change)
        except RuntimeError:
            print('faile')
            GPIO.remove_event_detect(pin)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=handle_gpio_change)

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    test_read_gpio_pins()
