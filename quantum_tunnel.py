from event_bus import KeyboardEventBus
from logger import log

class QuantumTunnel:
    def __init__(self):
        self.state = 'idle'

    def handle_event(self, event):
        log.debug("QuantumTunnel received event: %s", event)


def main():
    quantum_tunnel = QuantumTunnel()
    event_bus = KeyboardEventBus()
    event_bus.subscribe(quantum_tunnel)
    event_bus.wait_for_event()

if __name__ == "__main__":
    main()
