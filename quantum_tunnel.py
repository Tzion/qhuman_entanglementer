from event_bus import KeyboardEventBus, Subscriber
from logger import log
import time

class QuantumTunnel(Subscriber):
    def __init__(self):
        self.state = 'idle'

    def handle_event(self, event):
        log.debug("QuantumTunnel received event of type %s: %s ", event.type if hasattr(event.type) else None, event)
        if event.type == 'explain':
            self.handle_explain_event() 
        if event.type == 'contact':
            self.handle_contact_event()

    def handle_contact_event(self):
        # Add your code here to handle the 'contact' event
        pass

    def handle_explain_event(self):
        time.sleep(3)

        


def main():
    quantum_tunnel = QuantumTunnel()
    event_bus = KeyboardEventBus()
    event_bus.subscribe(quantum_tunnel)
    event_bus.wait_for_events()

if __name__ == "__main__":
    main()

import gtts
