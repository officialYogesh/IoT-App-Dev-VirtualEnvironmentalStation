import os
import sys
import warnings
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

# Suppress all warnings including urllib3
warnings.filterwarnings("ignore", category=Warning)
# Specifically suppress urllib3 warnings
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*50)
    print(f"{text:^50}")
    print("="*50 + "\n")

def print_status(text, value=None):
    """Print a formatted status message"""
    if value is not None:
        print(f"{text:<30}: {value}")
    else:
        print(text)

def print_sensor_data(data):
    """Print formatted sensor data"""
    print("\n" + "-"*50)
    print("SENSOR READINGS")
    print("-"*50)
    print(f"Temperature: {data['field1']:>6}°C")
    print(f"Humidity:    {data['field2']:>6}%")
    print(f"CO2:        {data['field3']:>6}ppm")
    print("-"*50 + "\n")

def create_sensor_charts(data):
    """Create line charts for latest sensor data"""
    # Prepare data
    timestamp = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    values = {
        'Temperature': float(data['field1']),
        'Humidity': float(data['field2']),
        'CO2': float(data['field3'])
    }
    
    # Create figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
    
    # Temperature chart
    ax1.plot([timestamp], [values['Temperature']], 'ro-', label='Temperature')
    ax1.set_title('Temperature Over Time')
    ax1.set_ylabel('Temperature (°C)')
    ax1.grid(True)
    ax1.legend()
    
    # Set y-axis range for temperature (-50 to 50)
    ax1.set_ylim(-50, 50)
    
    # Humidity chart
    ax2.plot([timestamp], [values['Humidity']], 'bo-', label='Humidity')
    ax2.set_title('Humidity Over Time')
    ax2.set_ylabel('Humidity (%)')
    ax2.grid(True)
    ax2.legend()
    
    # Set y-axis range for humidity (0 to 100)
    ax2.set_ylim(0, 100)
    
    # CO2 chart
    ax3.plot([timestamp], [values['CO2']], 'go-', label='CO2')
    ax3.set_title('CO2 Levels Over Time')
    ax3.set_ylabel('CO2 (ppm)')
    ax3.grid(True)
    ax3.legend()
    
    # Set y-axis range for CO2 (300 to 2000)
    ax3.set_ylim(300, 2000)
    
    # Format x-axis for all subplots
    for ax in [ax1, ax2, ax3]:
        plt.setp(ax.get_xticklabels(), rotation=45)
        # Set x-axis limits to show a small range around the timestamp
        time_padding = timedelta(minutes=15)
        ax.set_xlim(timestamp - time_padding, timestamp + time_padding)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the chart
    plt.savefig('latest_readings.png')
    print_status("Charts saved as 'latest_readings.png'")

def get_latest_data(channel_id):
    """Fetch the latest data from ThingSpeak channel"""
    try:
        # ThingSpeak API endpoint for latest data
        url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?results=1"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        if not data['feeds']:
            print_header("NO DATA AVAILABLE")
            print_status("No sensor data found for the specified channel")
            return None
            
        return data['feeds'][0]
        
    except requests.exceptions.RequestException as e:
        print_header("ERROR FETCHING DATA")
        print_status("Failed to connect to ThingSpeak API", str(e))
        return None
    except Exception as e:
        print_header("ERROR")
        print_status("An unexpected error occurred", str(e))
        return None

def main():
    """Main entry point"""
    # Get channel ID from environment or command line
    channel_id = os.getenv("CHANNEL_ID")
    if not channel_id:
        if len(sys.argv) > 1:
            channel_id = sys.argv[1]
        else:
            print_header("ERROR: Missing Channel ID")
            print_status("Please provide the channel ID either:")
            print_status("1. Set CHANNEL_ID in your .env file")
            print_status("2. Pass it as a command line argument")
            print_status("\nUsage: python display_latest_data.py <channel_id>")
            sys.exit(1)

    print_header("FETCHING LATEST SENSOR DATA")
    print_status("Channel ID", channel_id)
    
    # Fetch and display the latest data
    latest_data = get_latest_data(channel_id)
    if latest_data:
        print_status("Timestamp", latest_data['created_at'])
        print_sensor_data(latest_data)
        create_sensor_charts(latest_data)

if __name__ == "__main__":
    main() 