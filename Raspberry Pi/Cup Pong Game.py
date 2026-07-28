#upload to git
from machine import Pin
import time

# List of pins as defined in your setup
pins = [2, 3, 4, 5, 6, 7]
beam_sensors = []

# Initialize each pin with a pull-up resistor
for p in pins:
    beam_sensors.append(Pin(p, Pin.IN, Pin.PULL_UP))

# Track which sensors have already been triggered
# Once a sensor is 'True', it won't print again
broken_status = [False] * len(beam_sensors)

while True:
    for i in range(len(beam_sensors)):
        # Check if the beam is broken (Low) and hasn't been logged yet
        if beam_sensors[i].value() == 0 and not broken_status[i]:
            print(1)  # Only print the number 1
            broken_status[i] = True # Mark as triggered
            
    time.sleep(0.05)