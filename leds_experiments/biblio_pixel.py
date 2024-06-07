from BiblioPixelAnimations.simple.Fill import Fill
from bibliopixel.drivers.PiWS281X import PiWS281X
import BiblioPixelAnimations
from bibliopixel import LEDStrip
from BiblioPixelAnimations.circle.bloom import CircleBloom
from bibliopixel import LEDCircle

# Use the PWM interface on GPIO 18
driver = PiWS281X(num=287, gpio=18)

#led = LEDStrip(driver)
#anim = Fill(led)
rings=[[0, 41], [41, 82], [82, 123], [123, 164], [164, 205], [205, 246] ,[246, 287]]
led = LEDCircle(driver, rings=rings)

anim = CircleBloom(led)


import pdb;pdb.set_trace()
try:
    anim.run()
except KeyboardInterrupt:
    led.all_off()
    led.update()
