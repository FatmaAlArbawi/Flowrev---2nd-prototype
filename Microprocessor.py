import serial  # For serial communication with Arduino
import time  # For timing operations
import numpy as np  # For numerical operations
from scipy.signal import find_peaks  # For finding peaks in the signal

# Initialize serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust '/dev/ttyACM0' to match your Arduino's port

def read_sensor(duration=5, sample_rate=100):
    samples = []  # List to store sensor readings
    start_time = time.time()  # Record the start time
    while time.time() - start_time < duration:  # Run for specified duration
        if ser.in_waiting:  # Check if there's data available from Arduino
            # Read a line from serial, decode it, remove whitespace, and convert to int
            sample = int(ser.readline().decode().strip())
            samples.append(sample)  # Add the sample to our list
        time.sleep(1/sample_rate)  # Wait to achieve desired sample rate
    return np.array(samples)  # Convert list to numpy array and return

def calculate_heart_rate(samples, sample_rate):
    # Find peaks in the signal, with a minimum distance between peaks
    peaks, _ = find_peaks(samples, distance=sample_rate//2)
    if len(peaks) > 1:  # If we found at least two peaks
        # Calculate average time between peaks and convert to BPM
        heart_rate = 60 / np.mean(np.diff(peaks) / sample_rate)
        return heart_rate
    return 0  # Return 0 if we couldn't calculate a heart rate

try:
    while True:  # Main loop
        samples = read_sensor()  # Read sensor data for 5 seconds
        heart_rate = calculate_heart_rate(samples, 100)  # Calculate heart rate
        print(f"Estimated Heart Rate: {heart_rate:.2f} BPM")  # Print result
        time.sleep(1)  # Wait 1 second before next measurement

except KeyboardInterrupt:  # If user presses Ctrl+C
    ser.close()  # Close the serial connection
    print("Program terminated")  # Print termination message