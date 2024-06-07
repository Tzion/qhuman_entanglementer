from bibliopixel.animation import StripChannelTest
from bibliopixel.drivers.SPI.WS2801 import WS2801
import BiblioPixelAnimations
from bibliopixel import LEDStrip

# driver = WS281X(num=286, pin=18)
driver = WS2801(num=286)
led = LEDStrip(driver)
anim = StripChannelTest(led)

anim.run()