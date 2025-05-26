# Drone Database Telemetry Module

A minimalistic SQLite database interface for storing drone flight logs and object detections.

## Overview

This module provides an easy-to-use interface for:

1. Storing and retrieving drone flight telemetry data
2. Managing detection records with classification information

## Data Structure

### Flight Logs

Flight logs store telemetry data with the following structure:

```python
telemetry_data = {
    "Roll": [],          # List of roll values in degrees
    "Pitch": [],        # List of pitch values in degrees
    "Yaw": [],          # List of yaw values in degrees
    "Latitude": [],     # List of latitude coordinates
    "Longitude": [],    # List of longitude coordinates
    "Altitude": [],     # List of altitude values in meters
    "HDOP": [],         # Horizontal dilution of precision
    "VDOP": [],         # Vertical dilution of precision
    "Satellites": [],   # Number of GPS satellites
    "Flight_Mode": [],  # Flight mode (e.g., AUTO, LOITER)
    "Voltage": [],      # Battery voltage
    "Current": [],      # Battery current
    "Armed": []         # Armed status (boolean)
}
```

### Detections

Detections store object detection data with the following fields:

- `timestamp`: When the detection occurred
- `category`: Classification category (e.g., "Worker", "Hazard")
- `latitude`: GPS latitude coordinate
- `longitude`: GPS longitude coordinate
- `picture`: Optional path to the detection image
- `bhp`: Boolean flag for health and safety compliance
- `worker`: Boolean flag indicating if a worker was detected
- `change`: Boolean flag for change detection since first test flight

## Usage

### Basic Usage

```python
from src.db import DroneDB

# Initialize database
db = DroneDB("drone_data.db")

# Add flight log
timestamp = "2025-05-26T18:00:00Z"
telemetry_data = {...}  # See structure above
log_id = db.add_flight_log(timestamp, telemetry_data)

# Add detection
detection_id = db.add_detection(
    timestamp="2025-05-26T18:05:00Z",
    category="Worker",
    latitude=52.2297,
    longitude=21.0122,
    picture="/path/to/image.jpg",
    bhp=True,
    worker=True,
    change=False
)
```

### Flight Log Operations

```python
# Get a specific flight log
log = db.get_flight_log(log_id)

# Get all flight logs
logs = db.get_all_flight_logs()

# Delete a flight log
db.delete_flight_log(log_id)
```

### Detection Operations

```python
# Get a specific detection
detection = db.get_detection(detection_id)

# Get all detections
detections = db.get_all_detections()

# Update a detection
db.update_detection(
    detection_id=detection_id,
    category="Updated Category",
    bhp=False
)

# Delete a detection
db.delete_detection(detection_id)
```

## Running Tests

To run the tests:

```bash
python -m unittest src.test_db
```

## Example

To see a complete working example, run:

```bash
python main.py
```

This will demonstrate all available database operations for both flight logs and detections.