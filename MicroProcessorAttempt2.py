#Author: Fatma Al Arbawi

import serial  # Import serial library for communication with Arduino
import time  # Import time library for delays
import numpy as np  # Import numpy for numerical operations
from scipy.signal import find_peaks  # Import find_peaks for heart rate calculation


# Initialize serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()  # Clear any existing data in the serial buffer


THRESHOLD = 500  # Define threshold for motor activation (adjust as needed)


def read_sensors():
    if ser.in_waiting > 0:  # Check if there's data available from Arduino
        try:
            line = ser.readline().decode('utf-8').rstrip()  # Read and decode a line of data
            return list(map(float, line.split(',')))  # Convert data to list of floats
        except ValueError:
            return None  # Return None if data conversion fails
    return None  # Return None if no data available


def calculate_heart_rate(samples, sample_rate):
    # Find peaks in the signal
    peaks, _ = find_peaks(samples, distance=sample_rate//2)
    if len(peaks) > 1:
        # Calculate heart rate from time between peaks
        return 60 / np.mean(np.diff(peaks) / sample_rate)
    return 0  # Return 0 if not enough peaks found


def control_motor(eeg_value):
    if eeg_value < THRESHOLD:
        ser.write(b'1')  # Send command to turn motor on
    else:
        ser.write(b'0')  # Send command to turn motor off


try:
    while True:  # Main loop
        sensor_data = read_sensors()  # Read sensor data from Arduino
        if sensor_data:
            eeg, temp, hr, spo2 = sensor_data  # Unpack sensor data
            print(f"EEG: {eeg}, Temp: {temp}, HR: {hr}, SpO2: {spo2}")  # Print sensor data
            control_motor(eeg)  # Control motor based on EEG value
        time.sleep(0.1)  # Short delay to avoid overwhelming the serial connection


except KeyboardInterrupt:
    print("Program terminated")  # Print message when program is interrupted
    ser.close()  # Close serial connection