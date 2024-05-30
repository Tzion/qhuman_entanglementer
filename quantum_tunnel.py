from event_bus import KeyboardEventBus
import keyboard

class QuantumTunnel:

    def __init__(self):
        self.state = 'idle'


def handle_keyboard_event(event):
    # Handle keyboard event here
    print(f"Key '{event.name}' is {'pressed' if event.event_type == 'down' else 'released'}")


def read_keyboard_events(event_bus):
    while True:
        event = keyboard.read_event()
        event_bus.post(event)


def main():
    quantum_tunnel = QuantumTunnel()
    event_bus = KeyboardEventBus()
    event_bus.subscribe(quantum_tunnel)
    event_bus.wait_for_event()

if __name__ == "__main__":
    main()


def read_gpio_pins(event_bus):
    while True:
        # Read GPIO pin state here
        pin_state = False
        event_bus.post(pin_state)

def handle_gpio_event(event):
    if event:
        print("GPIO pin is high")
    else:
        print("GPIO pin is low")

class State:
    def __init__(self):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self):
        pass

    def handle_event(self, event):
        pass


