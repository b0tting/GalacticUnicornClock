# Galactic Unicorn scripts

For networked examples you need to make a `secrets.py` script which looks like:
```
WIFI_SSID = "..."
WIFI_PASSWORD = "..." 
```

`clock.py` is a clock with a slightly modified version of the rainbow example as the background.
The time synchronises using NTP on start and at 5am every day.  This sets to UTC, you can adjust the hour with the volume up/down buttons.

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
