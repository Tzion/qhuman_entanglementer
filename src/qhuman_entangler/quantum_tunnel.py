from event_bus import KeyboardEventBus, Subscriber, GpioEventBus
from logger import defaultLogger as log
from audio_manager import AudioPlayer
from leds_manager import LedsManager
import time

class QuantumTunnel(Subscriber):
    def __init__(self):
        self.state = 'idle'
        self.audio_player = AudioPlayer()
        self.leds_manager =  LedsManager()
    
    def start(self):
        self.leds_manager.run_sequence('idle')


    def handle_event(self, event):
        log.debug("QuantumTunnel received event of type %s: %s ", event.type if hasattr(event, 'type') else None, event)
        if event.type == 'explain':
            self.handle_explain_event() 
        if event.type == 'contact':
            self.handle_contact_event()

    def handle_contact_event(self):
        # Add your code here to handle the 'contact' event
        pass

    def handle_explain_event(self):
        self.audio_player.play_sound("media/speech/explain_short_hebrew.mp3")

        


def main():
    quantum_tunnel = QuantumTunnel()
    quantum_tunnel.start()
    event_bus = KeyboardEventBus()
    event_bus = GpioEventBus()
    event_bus.subscribe(quantum_tunnel)
    event_bus.wait_for_events()

if __name__ == "__main__":
    main()

