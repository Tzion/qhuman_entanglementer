from abc import ABC, abstractmethod
from types import SimpleNamespace
import keyboard
import RPi.GPIO as GPIO
import requests
import time
from logger import logging
log = logging.getLogger(__name__)

class Subscriber(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass


class EventBus(ABC):
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber: Subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber:Subscriber):
        self._subscribers.remove(subscriber)

    def post(self, event):
        for subscriber in self._subscribers:
            subscriber.handle_event(event)

    @abstractmethod
    def wait_for_events(self):
        pass



class GpioEventBus(EventBus):
    
    EXPLAIN_BUTTON_PIN = 9
    CONTACT_SENSOR_PIN = 26

    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GpioEventBus.EXPLAIN_BUTTON_PIN, GPIO.IN)
        GPIO.setup(GpioEventBus.CONTACT_SENSOR_PIN, GPIO.IN)
        self.last_read_explain = GPIO.input(GpioEventBus.EXPLAIN_BUTTON_PIN)
        self.last_read_contact = GPIO.input(GpioEventBus.CONTACT_SENSOR_PIN)
    
    @staticmethod
    def turn_button_on(pin):
        button_is_off = GPIO.input(pin) == GPIO.LOW
        if button_is_off:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(GPIO.HIGH)
            GPIO.setup(pin, GPIO.IN)

    def wait_for_events(self):
        log.info('Polling gpio events')
        while True:
            try:
                self.last_read_explain = self.post_event_if_pin_change(GpioEventBus.EXPLAIN_BUTTON_PIN, self.last_read_explain, 'explain')
                self.last_read_contact = self.post_event_if_pin_change(GpioEventBus.CONTACT_SENSOR_PIN, self.last_read_contact, 'contact')
                if (self.last_read_explain == GPIO.LOW):
                    time.sleep(3)
                    GpioEventBus.turn_button_on(GpioEventBus.EXPLAIN_BUTTON_PIN)
                # leds_maintain() # super dirty but it's late
                time.sleep(1.5)  # add a small delay to reduce CPU usage
            except Exception as e:
                    log.error('Error while waiting for gpio events: %s', e)
                    
    def post_event_if_pin_change(self, pin, last_read, event_type):
        new_read = GPIO.input(pin)
        if new_read != last_read:
            event = SimpleNamespace(pin=pin, value=new_read, type=event_type)
            log.debug('Notifying subscribers about gpio event: %s', event)
            self.post(event)
        return new_read


# TODO redesign
last_execution_time = 0

def leds_maintain():
    global last_execution_time
    current_time = time.time()
    if current_time - last_execution_time >= 5:
        try:
            response = requests.get('http://localhost:5000/maintain')
            log.info('Response from leds maintenance: %s', response.text)
            last_execution_time = current_time
        except Exception as e:
            log.error('Error while calling leds maintenance: %s', e)

class KeyboardEventBus(EventBus):
    def wait_for_events(self):
        log.info('Waiting for keyboard events')
        while True:
            try:
                event = keyboard.read_event()
                log.info('Received keyboard event: %s: %s', event, event.__dict__)
                if event.scan_code == 12:  # the buttun 'q'
                    event.type = 'contact'
                if event.scan_code == 14:  # the button 'e'
                    event.type = 'explain'
                self.post(event) 
            except Exception as e:
                log.error('Error while waiting for events: %s', e)

