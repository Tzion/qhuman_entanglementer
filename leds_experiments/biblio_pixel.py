from bibliopixel.animation import StripChannelTest
from bibliopixel.drivers.SPI import WS281X
import BiblioPixelAnimations
from bibliopixel import LEDStrip

driver = WS281X(num=286, pin=18)
led = LEDStrip(driver)
anim = StripChannelTest(led)

anim.run()