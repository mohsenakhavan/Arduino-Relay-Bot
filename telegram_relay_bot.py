#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Arduino Relay Telegram Bot
This script creates a Telegram bot that controls Arduino relays over serial connection.
Author: Mohsen Akhavan
"""

import asyncio
import logging
import serial
import sys
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from configparser import ConfigParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read config
config = ConfigParser()
try:
    config.read('config.ini')
    # Telegram Bot API token
    API_TOKEN = config['Telegram']['token']
    # Serial port
    SERIAL_PORT = config['Arduino']['port']
    BAUD_RATE = int(config['Arduino']['baud_rate'])
except:
    logger.error("Config file is missing or invalid! Please create config.ini")
    sys.exit(1)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Serial connection to Arduino
arduino = None

# Keyboard markup
def get_keyboard():
    builder = ReplyKeyboardBuilder()
    
    # Relay control buttons
    for i in range(1, 9):
        builder.add(KeyboardButton(text=f"Relay {i} ON"))
        builder.add(KeyboardButton(text=f"Relay {i} OFF"))
    
    # Set row width for relay controls
    builder.adjust(2)
    
    # Mode control buttons
    builder.row(
        KeyboardButton(text="Mode: Normal"),
        KeyboardButton(text="Mode: All ON")
    )
    builder.row(
        KeyboardButton(text="Mode: All OFF"),
        KeyboardButton(text="Mode: Alternating")
    )
    builder.row(
        KeyboardButton(text="Mode: Sequential"),
        KeyboardButton(text="Status")
    )
    
    return builder.as_markup(resize_keyboard=True)

# Connect to Arduino
def connect_to_arduino():
    global arduino
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for Arduino to reset
        return True
    except Exception as e:
        logger.error(f"Failed to connect to Arduino: {e}")
        return False

# Send command to Arduino
def send_command(command):
    if arduino and arduino.is_open:
        try:
            arduino.write(f"{command}\n".encode())
            time.sleep(0.1)
            response = arduino.readline().decode().strip()
            return response
        except Exception as e:
            logger.error(f"Error sending command to Arduino: {e}")
            return "Error: Communication with Arduino failed"
    else:
        return "Error: Arduino not connected"

# Command handlers
@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    """Send a welcome message and display keyboard."""
    await message.answer(
        "Welcome to Arduino Relay Bot!\n"
        "Use the keyboard to control relays and modes.",
        reply_markup=get_keyboard()
    )

@dp.message(Command(commands=["help"]))
async def cmd_help(message: types.Message):
    """Display help message."""
    await message.answer(
        "Arduino Relay Bot Commands:\n\n"
        "- Relay controls: Toggle individual relays ON/OFF\n"
        "- Modes:\n"
        "  • Normal: Manual control\n"
        "  • All ON: Turn all relays on\n"
        "  • All OFF: Turn all relays off\n"
        "  • Alternating: Alternate between odd and even relays\n"
        "  • Sequential: Activate one relay at a time in sequence\n"
        "- Status: Show current relay states\n\n"
        "Use the keyboard buttons to control the relays."
    )

@dp.message(F.text.startswith("Relay"))
async def handle_relay(message: types.Message):
    """Handle relay control commands."""
    try:
        # Parse command (e.g., "Relay 1 ON")
        parts = message.text.split()
        relay_num = int(parts[1])
        state = 1 if parts[2] == "ON" else 0
        
        # Send command to Arduino
        command = f"RELAY:{relay_num}:{state}"
        response = send_command(command)
        
        await message.answer(f"Command sent: {message.text}\nResponse: {response}")
    except Exception as e:
        await message.answer(f"Error processing relay command: {e}")

@dp.message(F.text.startswith("Mode:"))
async def handle_mode(message: types.Message):
    """Handle mode control commands."""
    try:
        # Parse mode (e.g., "Mode: Normal")
        mode_name = message.text.split(": ")[1]
        
        # Map mode names to numbers
        mode_map = {
            "Normal": 0,
            "All ON": 1,
            "All OFF": 2,
            "Alternating": 3,
            "Sequential": 4
        }
        
        mode_num = mode_map.get(mode_name, 0)
        
        # Send command to Arduino
        command = f"MODE:{mode_num}"
        response = send_command(command)
        
        await message.answer(f"Mode set to: {mode_name}\nResponse: {response}")
    except Exception as e:
        await message.answer(f"Error processing mode command: {e}")

@dp.message(F.text == "Status")
async def handle_status(message: types.Message):
    """Get the current status of all relays."""
    try:
        # Check all relay states (this is simplified - ideally Arduino would send all states)
        status_message = "Relay Status:\n"
        
        # This is a simplified approach - in a real implementation, 
        # you might want to implement a specific STATUS command in the Arduino code
        for i in range(1, 9):
            # We're just returning what we last sent, not the actual states
            status_message += f"Relay {i}: Checking...\n"
        
        await message.answer(status_message)
    except Exception as e:
        await message.answer(f"Error getting status: {e}")

@dp.message()
async def echo(message: types.Message):
    """Echo all other messages."""
    await message.answer("Unrecognized command. Please use the provided keyboard.")

async def on_startup():
    """Connect to Arduino when the bot starts."""
    if connect_to_arduino():
        logger.info("Connected to Arduino")
    else:
        logger.error("Failed to connect to Arduino")

async def on_shutdown():
    """Close Arduino connection when the bot shuts down."""
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        logger.info("Arduino connection closed")

async def main():
    # Setup before starting
    await on_startup()
    
    # Start the bot
    await dp.start_polling(bot)
    
    # Cleanup when done
    await on_shutdown()

if __name__ == '__main__':
    asyncio.run(main()) 