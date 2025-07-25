"""Database operations for HassBeam Connect Backend integration."""

import json
import logging
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

_LOGGER = logging.getLogger(__name__)


def init_db(path: str) -> None:
    """Initialize the SQLite database with required tables."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ir_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device TEXT NOT NULL,
                    action TEXT NOT NULL,
                    event_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            _LOGGER.debug("Database initialized successfully: %s", path)
    except sqlite3.Error as err:
        _LOGGER.error("Database initialization failed: %s", err)
        raise


def check_ir_code_exists(path: str, device: str, action: str) -> bool:
    """Check if an IR code with the same device and action already exists."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM ir_codes WHERE device = ? AND action = ?",
                (device, action)
            )
            count = cursor.fetchone()[0]
            exists = count > 0
            _LOGGER.debug("IR code exists check for %s.%s: %s", device, action, exists)
            return exists
    except sqlite3.Error as err:
        _LOGGER.error("Failed to check IR code existence: %s", err)
        return False


def save_ir_code(path: str, device: str, action: str, event_data: Dict[str, Any]) -> bool:
    """Save an IR code to the database."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            
            # Check for duplicates using a single query
            cursor.execute(
                "SELECT COUNT(*) FROM ir_codes WHERE device = ? AND action = ?",
                (device, action)
            )
            if cursor.fetchone()[0] > 0:
                _LOGGER.warning("IR code for %s.%s already exists", device, action)
                return False
            
            # Insert the new record
            cursor.execute(
                "INSERT INTO ir_codes (device, action, event_data) VALUES (?, ?, ?)",
                (device, action, json.dumps(event_data))
            )
            conn.commit()
            _LOGGER.debug("IR code saved: %s.%s", device, action)
            return True
            
    except sqlite3.Error as err:
        _LOGGER.error("Failed to save IR code: %s", err)
        return False
    except (TypeError, ValueError) as err:
        _LOGGER.error("Invalid data format: %s", err)
        return False


def delete_ir_code(path: str, code_id: int) -> bool:
    """Delete an IR code from the database by ID."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ir_codes WHERE id = ?", (code_id,))
            deleted_count = cursor.rowcount
            conn.commit()
            
            if deleted_count > 0:
                _LOGGER.debug("IR code deleted successfully: ID %d", code_id)
                return True
            else:
                _LOGGER.warning("No IR code found with ID %d", code_id)
                return False
                
    except sqlite3.Error as err:
        _LOGGER.error("Failed to delete IR code: %s", err)
        return False


def get_ir_codes(path: str, device: Optional[str] = None, action: Optional[str] = None, limit: int = 10) -> List[Tuple]:
    """Retrieve IR codes from the database with optional filtering."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            
            # Build query with dynamic WHERE clause
            query = "SELECT * FROM ir_codes"
            params = []
            conditions = []
            
            if device:
                conditions.append("device = ?")
                params.append(device)
            if action:
                conditions.append("action = ?")
                params.append(action)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            _LOGGER.debug("Retrieved %d IR codes", len(results))
            return results
            
    except sqlite3.Error as err:
        _LOGGER.error("Failed to retrieve IR codes: %s", err)
        return []


def get_ir_code_by_device_action(path: str, device: str, action: str) -> Optional[Dict[str, Any]]:
    """Retrieve a specific IR code by device and action."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, device, action, event_data, created_at FROM ir_codes WHERE device = ? AND action = ?",
                (device, action)
            )
            result = cursor.fetchone()
            
            if result:
                code_data = {
                    "id": result[0],
                    "device": result[1],
                    "action": result[2],
                    "event_data": json.loads(result[3]),
                    "created_at": result[4]
                }
                _LOGGER.debug("Retrieved IR code for %s.%s", device, action)
                return code_data
            else:
                _LOGGER.debug("No IR code found for %s.%s", device, action)
                return None
                
    except sqlite3.Error as err:
        _LOGGER.error("Failed to retrieve IR code: %s", err)
        return None
    except json.JSONDecodeError as err:
        _LOGGER.error("Failed to parse event data: %s", err)
        return None
