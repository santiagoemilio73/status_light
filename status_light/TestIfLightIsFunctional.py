import machine
import neopixel
import time

# Define the number of LEDs (16 x 16 = 256)
NUM_PIXELS = 256

# Set up Pin 0 (GP0) as the data output pin
data_pin = machine.Pin(14, machine.Pin.OUT)

# Initialize the matrix using the built-in NeoPixel driver
matrix = neopixel.NeoPixel(data_pin, NUM_PIXELS)

def clear_matrix():
    matrix.fill((0, 0, 0))
    matrix.write()

try:
    while True:
        # Fill Matrix Red
        matrix.fill((255, 0, 0))
        matrix.write()
        time.sleep(1)
        
        # Fill Matrix Green
        matrix.fill((0, 255, 0))
        matrix.write()
        time.sleep(1)
        
        # Fill Matrix Blue
        matrix.fill((0, 0, 255))
        matrix.write()
        time.sleep(1)

except KeyboardInterrupt:
    # Safely turn off all LEDs when you stop the program
    clear_matrix()
