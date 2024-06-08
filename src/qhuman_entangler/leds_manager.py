import time
from rpi_ws281x import *
import random
from random import randint
import threading
from logger import logging
from flask import Flask, request
log = logging.getLogger(__name__)


# LED strip configuration:
LED_COUNT      = 286      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 65     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Ring:
    def __init__(self, num_pixels):
        self.num_pixels = num_pixels
        self.pixels = [Color(0,0,0) for _ in range(num_pixels)]
        
    def setAllRingColor(self, color):
        for i in range(self.num_pixels):
            self.pixels[i] = color

# Define functions which animate LEDs in various ways.
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def random_color():
    return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0,255))


def colorWipe(strip, rings,  stop_event, color=random_color(), wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)


def theaterChase(strip, rings,  stop_event, color=random_color(), wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            if stop_event.is_set():
                return
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def rainbow(strip, rings, stop_event, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip,  rings, stop_event, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, rings, stop_event, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            if stop_event.is_set():
                return
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


# ChatGPT animations
def colorFade(strip, rings,  stop_event, color_start=random_color(), color_end=random_color(), wait_ms=50, steps=100):
    """Fade between two colors."""
    r_start, g_start, b_start = color_start >> 16, (color_start >> 8) & 255, color_start & 255
    r_end, g_end, b_end = color_end >> 16, (color_end >> 8) & 255, color_end & 255
    r_step = (r_end - r_start) / steps
    g_step = (g_end - g_start) / steps
    b_step = (b_end - b_start) / steps
    for i in range(steps):
        r = int(r_start + (r_step * i))
        g = int(g_start + (g_step * i))
        b = int(b_start + (b_step * i))
        color = Color(r, g, b)
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, color)
        strip.show()
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)

def spaceshipLaunch(strip, rings,  stop_event, color=random_color(), wait_ms=50):
    """Spaceship launch animation."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
        strip.show()
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)

def meteorShower(strip, rings,  stop_event, color=random_color(), wait_ms=18, iterations=randint(2,13)):
    """Meteor shower animation."""
    for j in range(iterations):
        for i in range(0, strip.numPixels(), 3):
            strip.setPixelColor(i, color)
            strip.show()
            if stop_event.is_set():
                return
            time.sleep(wait_ms/1000.0)
            strip.setPixelColor(i, 0)
            strip.show()
            if stop_event.is_set():
                return

def fireworks(strip, rings,  stop_event, wait_ms=randint(8,78), iterations=randint(2,8)):
    """Fireworks animation."""
    for j in range(iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, random_color())
            strip.show()
            if stop_event.is_set():
                return
            time.sleep(wait_ms/1000.0)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, 0)
        strip.show()
        if stop_event.is_set():
            return

def colorWipeRandom(strip, rings,  stop_event, wait_ms=10):
    """Wipe random color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, random_color())
        strip.show()
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)

def particalAccelerator(strip, rings, stop_event, color=random_color(), wait_ms=50):
    """Particle accelerator animation."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        wait_accelerate = wait_ms/(i+1) + wait_ms / 2
        if stop_event.is_set():
            return
        time.sleep(wait_accelerate/1000.0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
        strip.show()
        wait_accelerate = wait_ms/(i+1) + wait_ms / 2
        if stop_event.is_set():
            return
        time.sleep(wait_ms/1000.0)

def entanglement(strip,  rings, duration_ms, stop_event):
    """Shzira animation."""
    index = 0
    waveColor = random_color()
    start_time = time.time()
    time_left = duration_ms / 1000
    while time_left > 0:
        rings[index].setAllRingColor(waveColor)
        rings[-1-index].setAllRingColor(waveColor)
        writeRingsToStrip(strip, rings)
        
        if(index>=4): #start from the beginning with a new color
            index = 0
            waveColor = random_color()
            time.sleep(0.2)
        else: 
            index += 1
        time_left = (duration_ms / 1000) - (time.time() - start_time)
        time.sleep(0.07)
    # while not stop_event.is_set():
    #     for i in range(len(rings)):
    #         rings[i].setAllRingColor(random_color())
    #     writeRingsToStrip(strip, rings)
    #     time.sleep(2)


# helper for converting rings to strip and SHOW
def writeRingsToStrip(strip, rings):
    current_ring_index = 0
    forward = True
    for ring in rings:
        for i in range(ring.num_pixels):
            # set strip pixels between [current_ring_index, and current_ring_index + ring.num_pixels]
            if forward:
                strip.setPixelColor(current_ring_index + i, ring.pixels[i])
            else:
                strip.setPixelColor(current_ring_index + ring.num_pixels - 1 - i, ring.pixels[i])
                
        current_ring_index += ring.num_pixels
        forward = not forward
    strip.show()



class LedsManager():
    def __init__(self):
        log.info('Initializing leds manager')
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.idle_animations = [colorWipe, theaterChase, rainbow, rainbowCycle, theaterChaseRainbow,
                                colorFade, spaceshipLaunch, meteorShower, fireworks, colorWipeRandom, particalAccelerator]
        self.stop_event = threading.Event()
        self.animation_thread = None
        self.running_animation = None
        self.rings = [
            Ring(41),
            Ring(40),
            Ring(41),
            Ring(41), #middle ring
            Ring(41),
            Ring(41),
            Ring(41),
        ]    
    
    def run_animation(self, animation: callable, **kwargs):
        log.debug("Running leds animation in the background: %s by thread: %s", animation.__name__, 
                 threading.get_ident())
        self.stop_event.set()  # Signal the current animation to stop
        if self.animation_thread is not None:
            self.animation_thread.join()  # Wait for the current animation to stop
        self.stop_event.clear()  # Reset the stop event for the next animation
        self.animation_thread = threading.Thread(target=self._run_animation, args=(animation,), kwargs=kwargs)
        self.animation_thread.start()

    def _run_animation(self, animation: callable, **kwargs):
        try:
            self.running_animation = animation
            animation(self.strip, self.rings, stop_event=self.stop_event, **kwargs)
        except Exception as e:
            log.error("Error running leds animation: %s", e)
        finally:
            self.running_animation = None

    def stop_current_animation(self):
        log.info('signaling the current animation to stop')
        self.stop_event.set()
        if self.animation_thread is not None:
            self.animation_thread.join()

    def idle(self):
        if self.running_animation is None:
            animation = random.choice(self.idle_animations)
            self.run_animation(animation)



app = Flask(__name__)
leds_manager = LedsManager()

@app.route('/idle')
def idle():
    leds_manager.idle()
    return 'Idle mode activated'


@app.route('/entanglement')
def run_entanglement():
    duration_ms = int(float(request.args.get('duration_ms', 0)))
    leds_manager.run_animation(entanglement, duration_ms=duration_ms)
    return 'QUANTHUMANAZING!'

if __name__ == '__main__':
    app.run()
