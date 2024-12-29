import RPi.GPIO as GPIO
import sys

# Define PINs according to cabling
dataPIN = 16
latchPIN = 20
clockPIN = 21

# Set pins to output
GPIO.setmode(GPIO.BCM)
GPIO.setup((dataPIN, latchPIN, clockPIN), GPIO.OUT)

# Define shift register update function
def shift_update(input_data, data, clock, latch):
    # Ensure input data is 16 bits
    if len(input_data) != 16:
        raise ValueError("Input data must be 16 bits (e.g., '1111000011110000').")

    # Put latch down to start data sending
    GPIO.output(latch, 0)

    # Load data in reverse order
    for i in range(15, -1, -1):  # Iterate through all 16 bits
        GPIO.output(clock, 0)
        GPIO.output(data, int(input_data[i]))
        GPIO.output(clock, 1)

    # Put latch up to store data on the shift registers
    GPIO.output(latch, 1)

# Main program, calling shift register function
# Uses "sys.argv" to pass arguments from command line
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <16-bit-binary-string>")
        sys.exit(1)

    shift_update(sys.argv[1], dataPIN, clockPIN, latchPIN)

    # Clean up GPIO pins
    GPIO.cleanup()
