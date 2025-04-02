# Arduino Relay Bot - Circuit Diagram

## Connection Diagram

```
+---------------+          +------------------+
|               |          |                  |
|   Arduino     |          |   8-Channel      |
|    Uno        |          |  Relay Module    |
|               |          |                  |
+---+-+-+-+-+---+          +--+-+-+-+-+-+-+--+
    | | | | |                 | | | | | | |
    | | | | |                 | | | | | | |
    | | | | |                 | | | | | | |
    | | | | |                 | | | | | | |
    | | | | |                 | | | | | | |
    | | | | +-----------------+ | | | | | |
    | | | +-------------------+ | | | | | |
    | | +---------------------+ | | | | | |
    | +-----------------------+ | | | | | |
    +-------------------------+ | | | | | |
      5V --------------------- VCC | | | | |
      GND -------------------- GND | | | | |
      Pin 2 ------------------- IN1 | | | | |
      Pin 3 ------------------- IN2 | | | | |
      Pin 4 ------------------- IN3 | | | | |
      Pin 5 ------------------- IN4 | | | | |
      Pin 6 ------------------- IN5 | | | | |
      Pin 7 ------------------- IN6 | | | | |
      Pin 8 ------------------- IN7 | | | | |
      Pin 9 ------------------- IN8 | | | | |
                                 | | | | | | |
                                 v v v v v v v
                                 To your devices
                                (Connect COM and NO/NC)
```

## Detailed Connections

### Arduino to Relay Module

| Arduino Pin | Relay Module Pin | Description      |
|-------------|------------------|------------------|
| 5V          | VCC              | Power supply     |
| GND         | GND              | Ground           |
| D2          | IN1              | Relay 1 control  |
| D3          | IN2              | Relay 2 control  |
| D4          | IN3              | Relay 3 control  |
| D5          | IN4              | Relay 4 control  |
| D6          | IN5              | Relay 5 control  |
| D7          | IN6              | Relay 6 control  |
| D8          | IN7              | Relay 7 control  |
| D9          | IN8              | Relay 8 control  |

### Relay Module to Controlled Devices

For each relay on the module:

1. **COM** (Common) - Connect to your power source
2. **NO** (Normally Open) - Connect to your device for normally open operation (circuit is open when relay is OFF)
3. **NC** (Normally Closed) - Connect to your device for normally closed operation (circuit is closed when relay is OFF)

## Power Considerations

The relay module typically needs 5V power. If you're controlling high-power devices:

1. **External Power Supply**: Use a separate power supply for the relay module
2. **Ground Connection**: Always connect the Arduino GND to the relay module GND
3. **Power Rating**: Ensure your power supply can handle the current requirements of all relays

## Safety Warning

⚠️ **CAUTION**: Working with relays can involve high voltage electricity. If you're controlling mains voltage (110V/220V):

1. Ensure all connections are properly insulated
2. Use appropriate gauge wires for the current
3. If you're not experienced with electrical wiring, consult a qualified electrician
4. Disconnect power when making any changes to the circuit
5. Consider using a fuse for additional safety 