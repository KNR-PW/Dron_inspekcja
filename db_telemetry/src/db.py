import sqlite3
import json
import os
from typing import Dict, List, Optional, Tuple, Union, Any


class DroneDB:
    """Simple SQLite database interface for drone flight logs and detections."""

    def __init__(self, db_path: str = "drone_data.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Create tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create flight_logs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            telemetry_data TEXT NOT NULL
        )
        ''')
        
        # Create detections table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            category TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            picture TEXT,
            bhp INTEGER NOT NULL,
            worker INTEGER NOT NULL,
            change INTEGER NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()

    def _get_connection(self):
        """Get SQLite connection."""
        return sqlite3.connect(self.db_path)

    # Flight logs methods
    def add_flight_log(self, timestamp: str, telemetry_data: Dict[str, List]) -> int:
        """
        Add a flight log to the database.
        
        Args:
            timestamp: ISO timestamp of the flight log
            telemetry_data: Dictionary with telemetry data arrays
            
        Returns:
            id: The ID of the newly added flight log
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Convert telemetry data to JSON string
        telemetry_json = json.dumps(telemetry_data)
        
        cursor.execute(
            "INSERT INTO flight_logs (timestamp, telemetry_data) VALUES (?, ?)",
            (timestamp, telemetry_json)
        )
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return log_id

    def get_flight_log(self, log_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a flight log by ID.
        
        Args:
            log_id: The ID of the flight log to retrieve
            
        Returns:
            Dictionary with flight log data or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, timestamp, telemetry_data FROM flight_logs WHERE id = ?", (log_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "timestamp": result[1],
                "telemetry_data": json.loads(result[2])
            }
        return None

    def get_all_flight_logs(self) -> List[Dict[str, Any]]:
        """
        Get all flight logs.
        
        Returns:
            List of dictionaries with flight log data
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, timestamp, telemetry_data FROM flight_logs")
        results = cursor.fetchall()
        conn.close()
        
        logs = []
        for result in results:
            logs.append({
                "id": result[0],
                "timestamp": result[1],
                "telemetry_data": json.loads(result[2])
            })
        return logs

    def delete_flight_log(self, log_id: int) -> bool:
        """
        Delete a flight log by ID.
        
        Args:
            log_id: The ID of the flight log to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM flight_logs WHERE id = ?", (log_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted

    # Detection methods
    def add_detection(self, 
                     timestamp: str,
                     category: str,
                     latitude: float,
                     longitude: float,
                     picture: Optional[str] = None,
                     bhp: bool = False,
                     worker: bool = False,
                     change: bool = False) -> int:
        """
        Add a detection to the database.
        
        Args:
            timestamp: ISO timestamp of the detection
            category: Category of the detection
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            picture: Path to picture file (optional)
            bhp: Health and safety flag
            worker: Worker flag
            change: Change flag
            
        Returns:
            id: The ID of the newly added detection
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO detections 
               (timestamp, category, latitude, longitude, picture, bhp, worker, change) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (timestamp, category, latitude, longitude, picture, 
             1 if bhp else 0, 1 if worker else 0, 1 if change else 0)
        )
        
        detection_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return detection_id

    def get_detection(self, detection_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a detection by ID.
        
        Args:
            detection_id: The ID of the detection to retrieve
            
        Returns:
            Dictionary with detection data or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, category, latitude, longitude, picture, bhp, worker, change 
            FROM detections WHERE id = ?
        """, (detection_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "timestamp": result[1],
                "category": result[2],
                "latitude": result[3],
                "longitude": result[4],
                "picture": result[5],
                "bhp": bool(result[6]),
                "worker": bool(result[7]),
                "change": bool(result[8])
            }
        return None

    def get_all_detections(self) -> List[Dict[str, Any]]:
        """
        Get all detections.
        
        Returns:
            List of dictionaries with detection data
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, category, latitude, longitude, picture, bhp, worker, change 
            FROM detections
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        detections = []
        for result in results:
            detections.append({
                "id": result[0],
                "timestamp": result[1],
                "category": result[2],
                "latitude": result[3],
                "longitude": result[4],
                "picture": result[5],
                "bhp": bool(result[6]),
                "worker": bool(result[7]),
                "change": bool(result[8])
            })
        return detections

    def update_detection(self, 
                         detection_id: int,
                         timestamp: Optional[str] = None,
                         category: Optional[str] = None,
                         latitude: Optional[float] = None,
                         longitude: Optional[float] = None,
                         picture: Optional[str] = None,
                         bhp: Optional[bool] = None,
                         worker: Optional[bool] = None,
                         change: Optional[bool] = None) -> bool:
        """
        Update a detection by ID.
        
        Args:
            detection_id: The ID of the detection to update
            Other parameters: Optional new values
            
        Returns:
            True if updated successfully, False otherwise
        """
        # Get the current detection to fill in unspecified values
        current = self.get_detection(detection_id)
        if not current:
            return False
            
        # Use provided values or keep current ones
        new_timestamp = timestamp if timestamp is not None else current["timestamp"]
        new_category = category if category is not None else current["category"]
        new_latitude = latitude if latitude is not None else current["latitude"]
        new_longitude = longitude if longitude is not None else current["longitude"]
        new_picture = picture if picture is not None else current["picture"]
        new_bhp = 1 if (bhp if bhp is not None else current["bhp"]) else 0
        new_worker = 1 if (worker if worker is not None else current["worker"]) else 0
        new_change = 1 if (change if change is not None else current["change"]) else 0
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE detections 
            SET timestamp = ?, category = ?, latitude = ?, longitude = ?, 
                picture = ?, bhp = ?, worker = ?, change = ?
            WHERE id = ?
        """, (new_timestamp, new_category, new_latitude, new_longitude, 
              new_picture, new_bhp, new_worker, new_change, detection_id))
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated

    def delete_detection(self, detection_id: int) -> bool:
        """
        Delete a detection by ID.
        
        Args:
            detection_id: The ID of the detection to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM detections WHERE id = ?", (detection_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
