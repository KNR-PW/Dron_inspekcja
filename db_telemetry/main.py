import datetime
import os
from src.db import DroneDB


def generate_sample_telemetry():
    """Generate sample telemetry data for demonstration."""
    return {
        "Roll": [1.0, 1.5, 2.0, 2.5],
        "Pitch": [0.5, 0.7, 0.9, 1.1],
        "Yaw": [0.1, 0.2, 0.3, 0.4],
        "Latitude": [52.2297, 52.2298, 52.2299, 52.2300],
        "Longitude": [21.0122, 21.0123, 21.0124, 21.0125],
        "Altitude": [120.5, 121.0, 121.5, 122.0],
        "HDOP": [1.1, 1.2, 1.1, 1.0],
        "VDOP": [2.1, 2.0, 1.9, 1.8],
        "Satellites": [8, 9, 9, 10],
        "Flight_Mode": ["AUTO", "AUTO", "LOITER", "LOITER"],
        "Voltage": [12.1, 12.0, 11.9, 11.8],
        "Current": [10.5, 10.6, 10.7, 10.8],
        "Armed": [True, True, True, True]
    }


def demo_flight_logs(db):
    """Demonstrate flight log operations."""
    print("\n--- Flight Log Operations ---")
    
    # Add first flight log
    telemetry1 = generate_sample_telemetry()
    timestamp1 = datetime.datetime.now().isoformat()
    log_id1 = db.add_flight_log(timestamp1, telemetry1)
    print(f"Added flight log with ID: {log_id1}")
    
    # Add second flight log (will be kept in database)
    telemetry2 = generate_sample_telemetry()
    # Slightly modify telemetry data to make it different
    telemetry2["Altitude"] = [150.5, 151.0, 151.5, 152.0]
    telemetry2["Flight_Mode"] = ["LOITER", "RTL", "LAND", "DISARMED"]
    timestamp2 = datetime.datetime.now().isoformat()
    log_id2 = db.add_flight_log(timestamp2, telemetry2)
    print(f"Added second flight log with ID: {log_id2}")
    
    # Get the first flight log
    log = db.get_flight_log(log_id1)
    print(f"Retrieved flight log: ID={log['id']}, Timestamp={log['timestamp']}")
    print(f"Flight log has {len(log['telemetry_data']['Roll'])} data points")
    
    # Get all flight logs
    logs = db.get_all_flight_logs()
    print(f"Total flight logs in database: {len(logs)}")
    
    # Delete only the first flight log (keep the second one)
    deleted = db.delete_flight_log(log_id1)
    print(f"Deleted flight log {log_id1}: {deleted}")
    logs = db.get_all_flight_logs()
    print(f"Total flight logs after deletion: {len(logs)}")
    print(f"Remaining flight log ID: {logs[0]['id']}")
    print(f"Flight modes in remaining log: {logs[0]['telemetry_data']['Flight_Mode']}")
    


def demo_detections(db):
    """Demonstrate detection operations."""
    print("\n--- Detection Operations ---")
    
    # Add detections
    timestamp = datetime.datetime.now().isoformat()
    
    # Add worker detection
    worker_id = db.add_detection(
        timestamp=timestamp,
        category="Worker",
        latitude=52.2297,
        longitude=21.0122,
        picture="/path/to/worker.jpg",
        bhp=True, 
        worker=True,
        change=False
    )
    print(f"Added worker detection with ID: {worker_id}")
    
    # Add hazard detection
    hazard_id = db.add_detection(
        timestamp=timestamp,
        category="Hazard",
        latitude=52.2298,
        longitude=21.0123,
        bhp=False,  
        worker=False,
        change=True
    )
    print(f"Added hazard detection with ID: {hazard_id}")
    
    # Get a detection (workder dict)
    worker = db.get_detection(worker_id)
    print(f"Retrieved worker detection: ID={worker['id']}, Category={worker['category']}")
    print(f"Worker safety compliance: {worker['bhp']}")
    
    # Update a detection
    updated = db.update_detection(
        detection_id=hazard_id,
        category="Critical Hazard",
        bhp=False
    )
    print(f"Updated hazard detection: {updated}")
    
    hazard = db.get_detection(hazard_id)
    print(f"Updated category: {hazard['category']}")
    
    # Get all detections
    detections = db.get_all_detections()
    print(f"Total detections in database: {len(detections)}")
    
    # Delete a detection
    deleted = db.delete_detection(hazard_id)
    print(f"Deleted hazard detection: {deleted}")
    detections = db.get_all_detections()
    print(f"Total detections after deletion: {len(detections)}")


def main():
    """Main function demonstrating database operations."""
    print("Drone Database Example")
    
    # Clean up previous demo database if it exists
    db_path = "demo_drone_data.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Initialize database
    db = DroneDB(db_path)
    print(f"Initialized database at {db_path}")
    
    # Run demonstrations
    demo_flight_logs(db)
    demo_detections(db)
    
    print("\nDemo completed! Database operations demonstrated successfully. You can check the database file at {db_path}(with VSCode 4 example)")


if __name__ == "__main__":
    main()
