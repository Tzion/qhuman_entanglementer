import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
gpio_pins = list(range(2, 28))  # Read all GPIO pins on Raspberry Pi

def test_read_gpio_pins():
    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.IN)

    def handle_gpio_change(pin):
        print(f"GPIO pin {pin} changed")

    for pin in gpio_pins:
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=handle_gpio_change)

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()
