#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arduino Relay Test Script
Simple script to test the relay module connection with Arduino
Author: Mohsen Akhavan
"""

import serial
import time
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test Arduino relay module')
    parser.add_argument('port', help='Serial port (e.g., COM3, /dev/ttyACM0)')
    parser.add_argument('--baud', type=int, default=9600, help='Baud rate (default: 9600)')
    args = parser.parse_args()
    
    try:
        print(f"Connecting to Arduino on {args.port}...")
        # Connect to Arduino
        arduino = serial.Serial(args.port, args.baud, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        
        print("Connected! Starting relay test sequence.")
        
        # Test each relay
        for relay in range(1, 9):
            print(f"\nTesting Relay {relay}:")
            
            # Turn relay ON
            command = f"RELAY:{relay}:1\n"
            arduino.write(command.encode())
            time.sleep(0.1)
            response = arduino.readline().decode().strip()
            print(f"  ON  response: {response}")
            time.sleep(1)
            
            # Turn relay OFF
            command = f"RELAY:{relay}:0\n"
            arduino.write(command.encode())
            time.sleep(0.1)
            response = arduino.readline().decode().strip()
            print(f"  OFF response: {response}")
            time.sleep(0.5)
        
        # Test modes
        print("\nTesting operation modes:")
        
        # Mode 1: All ON
        print("\nMode: All ON")
        arduino.write(b"MODE:1\n")
        time.sleep(0.1)
        response = arduino.readline().decode().strip()
        print(f"  Response: {response}")
        time.sleep(3)
        
        # Mode 2: All OFF
        print("\nMode: All OFF")
        arduino.write(b"MODE:2\n")
        time.sleep(0.1)
        response = arduino.readline().decode().strip()
        print(f"  Response: {response}")
        time.sleep(1)
        
        # Mode 3: Alternating
        print("\nMode: Alternating (running for 5 seconds)")
        arduino.write(b"MODE:3\n")
        time.sleep(0.1)
        response = arduino.readline().decode().strip()
        print(f"  Response: {response}")
        time.sleep(5)
        
        # Mode 4: Sequential
        print("\nMode: Sequential (running for 10 seconds)")
        arduino.write(b"MODE:4\n")
        time.sleep(0.1)
        response = arduino.readline().decode().strip()
        print(f"  Response: {response}")
        time.sleep(10)
        
        # Back to normal mode
        print("\nReturning to Normal mode")
        arduino.write(b"MODE:0\n")
        time.sleep(0.1)
        response = arduino.readline().decode().strip()
        print(f"  Response: {response}")
        
        # Turn all relays off
        print("\nTurning all relays off")
        arduino.write(b"MODE:2\n")
        time.sleep(0.1)
        response = arduino.readline().decode().strip()
        
        print("\nTest completed successfully!")
        
        # Close the connection
        arduino.close()
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 