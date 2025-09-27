import unittest
import json
import sys
import os
from server import app
import sqlite3

class MoodJournalTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Use a test database
        self.test_db = "test_moods.db"
        app.config['DB'] = self.test_db
        
        # Initialize test DB
        with sqlite3.connect(self.test_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS moods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mood TEXT NOT NULL,
                    reason TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def tearDown(self):
        # Remove test DB after tests
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_health_check(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mood Journal API is up", response.data)

    def test_log_mood_success(self):
        data = {"mood": "grateful", "reason": "Testing"}
        response = self.client.post('/log', data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mood logged successfully", response.data)

    def test_log_mood_missing(self):
        data = {}  # No mood
        response = self.client.post('/log', data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Mood is required", response.data)

    def test_get_logs(self):
        # Insert a mood manually
        with sqlite3.connect(self.test_db) as conn:
            conn.execute("INSERT INTO moods (mood, reason) VALUES (?, ?)", ("grateful", "Unit test"))
        
        response = self.client.get('/logs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]['mood'], "grateful")

if __name__ == '__main__':
    unittest.main()
