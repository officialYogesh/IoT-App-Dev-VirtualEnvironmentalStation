# IoT Virtual Environmental Station

This project implements a cloud-based IoT system that collects environmental data from virtual sensors using the MQTT protocol. The system uses ThingSpeak as the cloud backend to store and visualize the sensor data.

## Project Overview

This project is part of CIS600 Internet of Things: Application Development (Spring 2025) Assignment 3. It implements a virtual environmental monitoring station that:

1. Simulates three environmental sensors:

   - Temperature (-50°C to 50°C)
   - Humidity (0% to 100%)
   - CO2 levels (300ppm to 2000ppm)

2. Publishes sensor data to ThingSpeak using MQTT protocol
3. Provides real-time visualization of sensor data
4. Stores historical data for analysis

## Features

- **Virtual Sensor Simulation**: Generates realistic environmental data
- **MQTT Communication**: Secure data transmission to ThingSpeak
- **Real-time Monitoring**: Live visualization of sensor readings
- **Historical Data**: Access to past sensor readings
- **Configurable Settings**: Easy customization of sensor ranges and update intervals

## Prerequisites

- Python 3.9 or higher
- ThingSpeak account
- MQTT credentials from ThingSpeak

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/IoT-App-Dev-VirtualEnvironmentalStation.git
cd IoT-App-Dev-VirtualEnvironmentalStation
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the template:

```bash
cp .env.example .env
```

5. Configure your `.env` file with your ThingSpeak credentials:

```bash
MQTT_USERNAME=your_username
MQTT_CLIENT_ID=your_client_id
MQTT_PASSWORD=your_password
CHANNEL_ID=your_channel_id
```

## Usage

1. Start the sensor simulation:

```bash
python sensor_simulation.py
```

2. View the data on ThingSpeak:
   - Visit your ThingSpeak channel
   - View real-time graphs
   - Access historical data

## Project Structure

```
IoT-App-Dev-VirtualEnvironmentalStation/
├── README.md
├── requirements.txt
├── .env.example
├── .env
└── sensor_simulation.py
```

## Implementation Details

### Virtual Sensors

- Temperature sensor: Generates random values between -50°C and 50°C
- Humidity sensor: Generates random values between 0% and 100%
- CO2 sensor: Generates random values between 300ppm and 2000ppm

### MQTT Communication

- Uses paho-mqtt library for MQTT protocol implementation
- Secure authentication using ThingSpeak credentials
- Automatic reconnection handling
- Error handling and logging

### Data Visualization

- Real-time graphs on ThingSpeak dashboard
- Historical data access
- Customizable display options

## Development Steps

1. Set up ThingSpeak account and create a channel
2. Configure MQTT credentials
3. Implement virtual sensor simulation
4. Set up MQTT communication
5. Implement data publishing
6. Configure visualization
7. Test and optimize

## License

This project is part of an academic assignment and is not intended for commercial use.

## Author

Yogesh Sanjay Patil
CIS600 Internet of Things: Application Development
Spring 2025
