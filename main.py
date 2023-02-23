import random
import time
import math
import network
import ntptime
import machine

try:
    from secrets import WIFI_SSID, WIFI_PASSWORD
except ImportError:
    print(
        "WiFi secrets are kept in secrets.py, please add them there and upload the secrets.py!"
    )
    raise
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

try:
    from unicorn_digits import NUMBERS, COLON, NUMBER_NONE
except ImportError:
    print(
        "Numbers are kept in unicorn_digits.py, please add them there and upload the numbers.py!"
    )
    raise
galactic = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT


def sync_time():
    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connect success or failure
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("waiting for connection...")
        time.sleep(1)

    if max_wait > 0 and wlan.status() >= 3:
        print("Connected")

        try:
            ntptime.settime()
            global utc_offset
            utc_offset = org_utc_offset
            print("Time set")
        except Exception as e:
            pass

    wlan.disconnect()
    wlan.active(False)


@micropython.native  # noqa: F821
def from_hv(h, v):
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    v *= 255.0
    p = 0.0
    q = v * (1.0 - f)
    t = v * f

    i = int(i) % 6
    if i == 0:
        return int(v), int(t), int(p)
    if i == 1:
        return int(q), int(v), int(p)
    if i == 2:
        return int(p), int(v), int(t)
    if i == 3:
        return int(p), int(q), int(v)
    if i == 4:
        return int(t), int(p), int(v)
    if i == 5:
        return int(v), int(p), int(q)


@micropython.native  # noqa: F821
def draw_rainbow():
    phase_percent = (time.ticks_ms() % 60000) * 0.000104719755 * 4
    for x in range(width):
        for y in range(height):
            y = y + random.randint(-1, 2)
            v = (math.sin((x + y) / stripe_width + phase_percent) + 1.5) / 6.0
            colour = from_hv(((x - 1) % width) / width, v)

            graphics.set_pen(graphics.create_pen(*colour))
            graphics.pixel(x, y)


stripe_width = 6.0


light = 10
old_day = 0
old_hour = 4
org_utc_offset = 1
utc_offset = org_utc_offset
minutes_offset = 0
brightness_adjust = 0.2
clear_pen = graphics.create_pen(0, 0, 0)

up_button = machine.Pin(
    GalacticUnicorn.SWITCH_VOLUME_UP, machine.Pin.IN, machine.Pin.PULL_UP
)
down_button = machine.Pin(
    GalacticUnicorn.SWITCH_VOLUME_DOWN, machine.Pin.IN, machine.Pin.PULL_UP
)

white_pen = graphics.create_pen(255, 255, 255)
grey_pen = graphics.create_pen(30, 30, 30)
none_pen = graphics.create_pen(0, 0, 0)
pens = [none_pen, white_pen, grey_pen]


def draw_number(number, offset):
    for i in range(len(number)):
        for j in range(len(number[0])):
            if number[i][j] > 0:
                graphics.set_pen(pens[number[i][j]])
                graphics.pixel(offset + j, i)


def set_up_characters(hour, minute):
    number_collection = []
    if hour < 10:
        number_collection.append(NUMBER_NONE)
        number_collection.append(NUMBERS[hour])
    else:
        number_collection.append(NUMBERS[hour // 10])
        number_collection.append(NUMBERS[hour % 10])
    number_collection.append(COLON)
    number_collection.append(NUMBERS[minute // 10])
    number_collection.append(NUMBERS[minute % 10])
    return number_collection


def draw_clock(number_collection):
    offset = 4
    for number in number_collection:
        draw_number(number, offset)
        offset += len(number[0])


up_button.irq(
    trigger=machine.Pin.IRQ_FALLING,
    handler=lambda x: globals().update(utc_offset=(utc_offset + 1) % 24),
)

down_button.irq(
    trigger=machine.Pin.IRQ_FALLING,
    handler=lambda x: globals().update(minutes_offset=(minutes_offset + 1) % 60),
)

while True:
    if galactic.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
        brightness_adjust *= 1.05

    if galactic.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
        brightness_adjust *= 0.95

    if galactic.is_pressed(GalacticUnicorn.SWITCH_A):
        sync_time()

    if galactic.is_pressed(GalacticUnicorn.SWITCH_D):
        brightness_adjust = 1.0

    light = light * 0.9 + galactic.light() * 0.1
    if light < 10:
        graphics.set_pen(clear_pen)
        graphics.clear()
        galactic.set_brightness(0.04 * brightness_adjust)
    else:
        galactic.set_brightness(0.014 * light * brightness_adjust)
        draw_rainbow()

    year, month, day, hour, minute, second, _, _ = time.localtime()
    hour = (hour + utc_offset) % 24
    minute = (minute + minutes_offset) % 60
    digits = set_up_characters(hour, minute)
    draw_clock(digits)

    galactic.update(graphics)
    time.sleep(0.01)

    # Get time at start (after first draw), and at 5am every day
    if old_hour != hour:
        if old_hour == 4 and old_day != day:
            sync_time()
            old_day = day

        old_hour = hour
