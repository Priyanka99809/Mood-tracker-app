import unittest
import json
from server import app, db, Mood

class MoodJournalTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # in-memory DB
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = app.test_client()

        # Create tables
        with app.app_context():
            db.create_all()
            # Insert a test mood
            test_mood = Mood(mood="grateful", reason="Unit test")
            db.session.add(test_mood)
            db.session.commit()

    def tearDown(self):
        # Drop tables
        with app.app_context():
            db.drop_all()

    def test_health_check(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Mood Journal API is up", response.data)

    def test_log_mood_success(self):
        data = {"mood": "happy", "reason": "Testing"}
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
        response = self.client.get('/logs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['mood'], "grateful")  # the one inserted in setUp

if __name__ == '__main__':
    unittest.main()
