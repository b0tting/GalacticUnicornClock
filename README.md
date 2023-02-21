# Galactic Unicorn scripts

The [Galactic Unicorn](https://shop.pimoroni.com/products/galactic-unicorn) is a (near) 600 leds board made by Pimoroni, with a Raspberry Pico 2040 on board as controller. It's quit fun to program with Python. This script sets up a clock with easily modifiable multi-colored numbers.

Pimoroni sadly has no diffusers for the GU, but you can find "acryl diffuser sheets" on any of the big online shops. I dremeled one in shape and it really adds to the effect of the GU.     


# Setup
You can use the buttons to set the time, but you can also use an online NTP service. In that case the clock requires a wifi connection. You need to make a `secrets.py` script which looks like:
```
WIFI_SSID = "..."
WIFI_PASSWORD = "..." 
```
The time synchronises using NTP on start and at 5am every day. You might need to change the hour as the time retrieved is in UTC. 

![clock.jpg](clock.jpg)

To modify the numbers, see the "numbers.py" file. The digits in the array represent the pen colors in the "pens" array. 

### Button functions
| Button | Function            |
|--------|---------------------|
| VOL +  | Increase hour       |
| VOL -  | Increase minutes    |
| zzz    | Sync time with NTP  |
| LUX +  | Increase brightness |
| LUX -  | Decrease brightness |
