# Arduino Relay Bot

A complete IoT solution for controlling an 8-channel relay module using an Arduino Uno, integrated with a Telegram bot for remote control.

## Features

- Control 8 relays individually via Telegram
- User-friendly keyboard interface
- Multiple operation modes:
  - Normal: Manual control of each relay
  - All ON: Activate all relays
  - All OFF: Deactivate all relays
  - Alternating: Alternate between odd and even relays
  - Sequential: Activate one relay at a time in sequence
- Real-time status updates
- Easy to set up and configure

## Hardware Requirements

- Arduino Uno (or compatible board)
- 8-Channel Relay Module
- Computer or Raspberry Pi (to run the Python script)
- USB cable (to connect Arduino to the computer)
- Jumper wires

## Software Requirements

- Python 3.7 or higher
- Arduino IDE
- Required Python packages (see Installation section)

## Hardware Setup

1. Connect the relay module to Arduino:
   - VCC to 5V
   - GND to GND
   - IN1 to Digital Pin 2
   - IN2 to Digital Pin 3
   - IN3 to Digital Pin 4
   - IN4 to Digital Pin 5
   - IN5 to Digital Pin 6
   - IN6 to Digital Pin 7
   - IN7 to Digital Pin 8
   - IN8 to Digital Pin 9

2. Connect Arduino to your computer or Raspberry Pi via USB.

**For detailed wiring instructions with diagrams, see [CIRCUIT.md](CIRCUIT.md)**

## Software Installation

### Arduino Setup

1. Open the Arduino IDE
2. Copy the content of `arduino_relay_bot.ino` into a new sketch
3. Upload the sketch to your Arduino board

### Telegram Bot Setup

1. Create a new Telegram bot:
   - Start a chat with BotFather (@BotFather) on Telegram
   - Send the `/newbot` command and follow the instructions
   - Copy your bot's API token

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Edit `config.ini`
   - Replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` with your actual bot token
   - Set the correct serial port (e.g., `COM3` on Windows, `/dev/ttyACM0` on Linux, `/dev/cu.usbmodem14101` on macOS)

## Testing the Setup

Before running the full Telegram bot, you can verify that your Arduino and relay module are working correctly:

1. Make sure the Arduino is connected and has the sketch uploaded
2. Run the test script with your serial port:
   ```bash
   python test_relays.py COM3  # Replace COM3 with your port
   ```
   
The test script will:
- Test each relay individually
- Run through all operation modes
- Provide feedback on the responses from Arduino

This helps ensure that your hardware setup is correct before proceeding with the Telegram bot.

## Usage

1. Connect your Arduino to the computer
2. Run the Python script:
   ```bash
   python telegram_relay_bot.py
   ```

3. Start a chat with your bot on Telegram and send the `/start` command
4. Use the keyboard interface to control relays:
   - "Relay X ON" - Turn on relay X
   - "Relay X OFF" - Turn off relay X
   - "Mode: Normal" - Manual control mode
   - "Mode: All ON" - Turn all relays on
   - "Mode: All OFF" - Turn all relays off
   - "Mode: Alternating" - Alternate between odd and even relays
   - "Mode: Sequential" - Activate one relay at a time in sequence
   - "Status" - Check the current status of all relays

## Troubleshooting

### Arduino Not Detected

- Check if the Arduino is properly connected to the computer
- Verify the correct serial port is selected in `config.ini`
- Try different USB cables or ports

### Telegram Bot Not Responding

- Ensure the bot token is correctly set in `config.ini`
- Check if the Python script is running without errors
- Verify your internet connection

### Relays Not Switching

- Check the wiring between Arduino and relay module
- Verify that the relay module is properly powered
- Test the relay module separately to ensure it's functioning
- Run the `test_relays.py` script to verify communication with the Arduino

## Advanced Usage

### Custom Modes

You can modify the Arduino sketch to add custom operation modes:

1. Add a new mode to the `Mode` enum in `arduino_relay_bot.ino`
2. Implement the mode logic in the `handleMode()` function
3. Update the Telegram bot's mode mapping in `telegram_relay_bot.py`

### Multiple Users

By default, the bot responds to all users. For security, you may want to restrict access:

1. Edit `telegram_relay_bot.py`
2. Add a list of authorized user IDs
3. Modify message handlers to check if the user's ID is in the authorized list

## Project Structure

- `arduino_relay_bot.ino`: Arduino sketch for controlling relays
- `telegram_relay_bot.py`: Python script for the Telegram bot
- `test_relays.py`: Test script to verify hardware setup
- `config.ini`: Configuration file for the bot
- `CIRCUIT.md`: Detailed circuit diagram and wiring instructions
- `requirements.txt`: Python dependencies

## License

This project is open-source and available under the MIT License.

## Author

Mohsen Akhavan

## Acknowledgements

- [Aiogram](https://github.com/aiogram/aiogram) - Telegram Bot framework
- [PySerial](https://github.com/pyserial/pyserial) - Serial communication library 