from event_bus import KeyboardEventBus, Subscriber, GpioEventBus
from logger import defaultLogger as log
from audio_manager import AudioPlayer
import RPi.GPIO as GPIO
import time
import threading
import requests

class QuantumTunnel(Subscriber):
    def __init__(self):
        log.info('Initializing QuantumTunnel')
        self.state = 'idle'
        self.audio_player = AudioPlayer()
    
    def start(self):
        pass


    def handle_event(self, event):
        log.debug("QuantumTunnel received event of type %s: %s ", event.type if hasattr(event, 'type') else None, event)
        if event.type == 'explain':
            self.handle_explain_event(event) 
        if event.type == 'contact':
            self.handle_contact_event(event)

    def handle_contact_event(self, event):
        if event.value == GPIO.HIGH:
            try:
                log.info('Starting entanglement!')
                self.audio_player.play_entanglement_with_leds()
            except Exception as e:
                log.error('Error while playing entanglement: %s', e)

    def handle_explain_event(self, event):
        if event.value == GPIO.LOW:
            try:
                self.audio_player.play_explain()
            except Exception as e:
                log.error('Error while playing explain: %s', e)


def main():
    quantum_tunnel = QuantumTunnel()
    quantum_tunnel.start()
    # event_bus = KeyboardEventBus()
    event_bus = GpioEventBus()
    event_bus.subscribe(quantum_tunnel)
    event_bus.wait_for_events()

if __name__ == "__main__":
    main()

