from BiblioPixelAnimations.simple.Fill import Fill
from bibliopixel.drivers.PiWS281X import PiWS281X
import BiblioPixelAnimations
from bibliopixel import LEDStrip

# Use the PWM interface on GPIO 18
driver = PiWS281X(num=286, gpio=18)

led = LEDStrip(driver)
anim = Fill(led)

try:
    anim.run()
except KeyboardInterrupt:
    led.all_off()
    led.update()