import serial
import sys
import tty
import termios
import select
import time

PORT = "/dev/ttyACM0"

ser = serial.Serial(PORT, 115200, timeout=0)
time.sleep(2)

def send(command):
    ser.write((command + "\n").encode())
    ser.flush()

# Initial setup
send("MODE DRAW")
send("CLEAR")

x = 8
y = 8
brightness = 15

colors = [
    (0, 180, 255),
    (255, 0, 0),
    (0, 255, 0),
    (255, 100, 0),
    (180, 0, 255),
]

color_index = 0

def show_cursor():
    send(f"CURSOR {x} {y}")

def get_key():
    if select.select([sys.stdin], [], [], 0.05)[0]:
        return sys.stdin.read(1)
    return None

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

print("\n================================")
print("     ROBOBOAT CONTROL CENTER")
print("================================")
print("1 - RADAR")
print("2 - SONAR")
print("3 - RAINBOW")
print("4 - WARNING")
print("5 - SYSTEM BOOT")
print("6 - SCANNER")
print("7 - HEARTBEAT")
print("0 - OFF")
print()
print("WASD - Move drawing cursor")
print("E - Draw pixel")
print("X - Erase pixel")
print("R - Change drawing color")
print("F - Fill entire matrix")
print("C - Clear matrix")
print("+/- - Brightness")
print("SPACE - Emergency OFF")
print("Q - Quit")
print("================================")

try:
    tty.setraw(fd)

    while True:
        key = get_key()

        if key is None:
            continue

        key = key.lower()

        if key == "q":
            break

        elif key == "1":
            send("MODE RADAR")

        elif key == "2":
            send("MODE SONAR")

        elif key == "3":
            send("MODE RAINBOW")

        elif key == "4":
            send("MODE WARNING")

        elif key == "5":
            send("MODE BOOT")

        elif key == "6":
            send("MODE SCAN")

        elif key == "7":
            send("MODE HEART")

        elif key == "0" or key == " ":
            send("OFF")

        elif key == "w":
            y = max(0, y - 1)
            send("MODE DRAW")
            show_cursor()

        elif key == "s":
            y = min(15, y + 1)
            send("MODE DRAW")
            show_cursor()

        elif key == "a":
            x = max(0, x - 1)
            send("MODE DRAW")
            show_cursor()

        elif key == "d":
            x = min(15, x + 1)
            send("MODE DRAW")
            show_cursor()

        elif key == "e":
            send("MODE DRAW")
            r, g, b = colors[color_index]
            send(f"PIXEL {x} {y} {r} {g} {b}")

        elif key == "x":
            send("MODE DRAW")
            send(f"PIXEL {x} {y} 0 0 0")

        elif key == "r":
            color_index = (color_index + 1) % len(colors)
            print("\nColor changed:", colors[color_index])

        elif key == "f":
            r, g, b = colors[color_index]
            send(f"COLOR {r} {g} {b}")

        elif key == "c":
            send("MODE DRAW")
            send("CLEAR")

        elif key == "+" or key == "=":
            brightness = min(100, brightness + 5)
            send(f"BRIGHT {brightness}")

        elif key == "-":
            brightness = max(1, brightness - 5)
            send(f"BRIGHT {brightness}")

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    send("OFF")
    ser.close()
    print("\nController disconnected.")

