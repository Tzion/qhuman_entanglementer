import RPi.GPIO as GPIO
import time
from gpiozero import Button

GPIO.setmode(GPIO.BCM)
gpio_pins = list(range(2, 28))  # Read all GPIO pins on Raspberry Pi

def test_read_gpio_pins():
    def handle_gpio_change(pin):
        print(f"GPIO pin {pin} changed")

    for pin in gpio_pins:
        GPIO.setup(pin, GPIO.IN)
        try:
            print(f"adding event detection for pin {pin}")
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=handle_gpio_change)
        except RuntimeError:
            GPIO.remove_event_detect(pin)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=handle_gpio_change)

    try:
        while True:
            pass

    except KeyboardInterrupt:
        GPIO.cleanup()


def test_poll_gpio():
    while True:
        for pin in gpio_pins:
            GPIO.setup(pin, GPIO.IN)
            print(f"GPIO pin {pin} is {GPIO.input(pin)}")
        time.sleep(0.1)
    

def test_read_gpio_pins__gpiozero():

        def handle_gpio_change(pin):
            print(f"GPIO pin {pin} changed")

        buttons = [Button(pin) for pin in gpio_pins]

        for button in buttons:
            print(f"adding event detection for pin {button}")
            button.when_pressed = handle_gpio_change
            button.when_released = handle_gpio_change
        while True:
            pass

if __name__ == "__main__":
    test_poll_gpio()
