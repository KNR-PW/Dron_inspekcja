import unittest
import os
import datetime
from .db import DroneDB


class TestDroneDB(unittest.TestCase):
    """Test cases for DroneDB class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_db_path = "test_drone_data.db"
        # Ensure test database doesn't exist
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
        self.db = DroneDB(self.test_db_path)
        
        # Sample telemetry data for testing
        self.sample_telemetry = {
            "Roll": [1.0, 2.0, 3.0],
            "Pitch": [0.5, 1.5, 2.5],
            "Yaw": [0.1, 0.2, 0.3],
            "Latitude": [52.1, 52.2, 52.3],
            "Longitude": [21.1, 21.2, 21.3],
            "Altitude": [100.0, 110.0, 120.0],
            "HDOP": [1.1, 1.2, 1.3],
            "VDOP": [2.1, 2.2, 2.3],
            "Satellites": [8, 9, 10],
            "Flight_Mode": ["AUTO", "AUTO", "LOITER"],
            "Voltage": [12.1, 12.0, 11.9],
            "Current": [10.5, 10.6, 10.7],
            "Armed": [True, True, True]
        }
        
        # Sample timestamp
        self.timestamp = datetime.datetime.now().isoformat()
    
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    # Flight Log Tests
    def test_add_get_flight_log(self):
        """Test adding and retrieving a flight log."""
        # Add flight log
        log_id = self.db.add_flight_log(self.timestamp, self.sample_telemetry)
        
        # Verify log_id is valid
        self.assertIsNotNone(log_id)
        self.assertGreater(log_id, 0)
        
        # Get flight log
        log = self.db.get_flight_log(log_id)
        
        # Verify retrieved log
        self.assertIsNotNone(log)
        self.assertEqual(log["id"], log_id)
        self.assertEqual(log["timestamp"], self.timestamp)
        self.assertEqual(log["telemetry_data"], self.sample_telemetry)
    
    def test_get_all_flight_logs(self):
        """Test retrieving all flight logs."""
        # Add multiple flight logs
        log_id1 = self.db.add_flight_log(self.timestamp, self.sample_telemetry)
        
        # Modify the timestamp slightly for the second log
        timestamp2 = datetime.datetime.now().isoformat()
        log_id2 = self.db.add_flight_log(timestamp2, self.sample_telemetry)
        
        # Get all logs
        logs = self.db.get_all_flight_logs()
        
        # Verify both logs are retrieved
        self.assertEqual(len(logs), 2)
        log_ids = [log["id"] for log in logs]
        self.assertIn(log_id1, log_ids)
        self.assertIn(log_id2, log_ids)
    
    def test_delete_flight_log(self):
        """Test deleting a flight log."""
        # Add flight log
        log_id = self.db.add_flight_log(self.timestamp, self.sample_telemetry)
        
        # Verify log exists
        self.assertIsNotNone(self.db.get_flight_log(log_id))
        
        # Delete log
        result = self.db.delete_flight_log(log_id)
        
        # Verify deletion was successful
        self.assertTrue(result)
        
        # Verify log no longer exists
        self.assertIsNone(self.db.get_flight_log(log_id))
        
        # Try to delete non-existent log
        result = self.db.delete_flight_log(999)
        self.assertFalse(result)
    
    # Detection Tests
    def test_add_get_detection(self):
        """Test adding and retrieving a detection."""
        # Add detection
        detection_id = self.db.add_detection(
            timestamp=self.timestamp,
            category="Person",
            latitude=52.1,
            longitude=21.1,
            picture="path/to/image.jpg",
            bhp=True,
            worker=True,
            change=False
        )
        
        # Verify detection_id is valid
        self.assertIsNotNone(detection_id)
        self.assertGreater(detection_id, 0)
        
        # Get detection
        detection = self.db.get_detection(detection_id)
        
        # Verify retrieved detection
        self.assertIsNotNone(detection)
        self.assertEqual(detection["id"], detection_id)
        self.assertEqual(detection["timestamp"], self.timestamp)
        self.assertEqual(detection["category"], "Person")
        self.assertEqual(detection["latitude"], 52.1)
        self.assertEqual(detection["longitude"], 21.1)
        self.assertEqual(detection["picture"], "path/to/image.jpg")
        self.assertTrue(detection["bhp"])
        self.assertTrue(detection["worker"])
        self.assertFalse(detection["change"])
    
    def test_get_all_detections(self):
        """Test retrieving all detections."""
        # Add multiple detections
        detection_id1 = self.db.add_detection(
            timestamp=self.timestamp,
            category="Person",
            latitude=52.1,
            longitude=21.1,
            bhp=True,
            worker=True,
            change=False
        )
        
        # Modify the timestamp slightly for the second detection
        timestamp2 = datetime.datetime.now().isoformat()
        detection_id2 = self.db.add_detection(
            timestamp=timestamp2,
            category="Vehicle",
            latitude=52.2,
            longitude=21.2,
            bhp=False,
            worker=False,
            change=True
        )
        
        # Get all detections
        detections = self.db.get_all_detections()
        
        # Verify both detections are retrieved
        self.assertEqual(len(detections), 2)
        detection_ids = [d["id"] for d in detections]
        self.assertIn(detection_id1, detection_ids)
        self.assertIn(detection_id2, detection_ids)
    
    def test_update_detection(self):
        """Test updating a detection."""
        # Add detection
        detection_id = self.db.add_detection(
            timestamp=self.timestamp,
            category="Person",
            latitude=52.1,
            longitude=21.1,
            bhp=True,
            worker=True,
            change=False
        )
        
        # Update detection
        result = self.db.update_detection(
            detection_id=detection_id,
            category="Worker",
            latitude=52.5,
            bhp=False
        )
        
        # Verify update was successful
        self.assertTrue(result)
        
        # Get updated detection
        detection = self.db.get_detection(detection_id)
        
        # Verify updated fields
        self.assertEqual(detection["category"], "Worker")
        self.assertEqual(detection["latitude"], 52.5)
        self.assertFalse(detection["bhp"])
        # Verify non-updated fields remain the same
        self.assertEqual(detection["longitude"], 21.1)
        self.assertTrue(detection["worker"])
        self.assertFalse(detection["change"])
        
        # Try to update non-existent detection
        result = self.db.update_detection(detection_id=999, category="Non-existent")
        self.assertFalse(result)
    
    def test_delete_detection(self):
        """Test deleting a detection."""
        # Add detection
        detection_id = self.db.add_detection(
            timestamp=self.timestamp,
            category="Person",
            latitude=52.1,
            longitude=21.1,
            bhp=False,
            worker=True,
            change=False
        )
        
        # Verify detection exists
        self.assertIsNotNone(self.db.get_detection(detection_id))
        
        # Delete detection
        result = self.db.delete_detection(detection_id)
        
        # Verify deletion was successful
        self.assertTrue(result)
        
        # Verify detection no longer exists
        self.assertIsNone(self.db.get_detection(detection_id))
        
        # Try to delete non-existent detection
        result = self.db.delete_detection(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
