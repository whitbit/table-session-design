import unittest
from controller import Session, Event, SessionController
from datetime import datetime, timedelta

class SessionTestCase(unittest.TestCase):

    def setUp(self):
        self.test_session = SessionController()
        self.touch_1 = Event('touch', 10)
        self.touch_2 = Event('touch', 5)
        self.check_open = Event('check_open')
        self.check_close = Event('check_close')

    def testTouchEvent1(self):
        """
        Adds touch event with default time and asserts session is in progress.
        Asserts session end time.

        """
        self.test_session.add_event(self.touch_1, 5)
        start_time = self.test_session.session.start

        self.assertIsNotNone(self.test_session.session)
        self.assertEqual(self.test_session.session.end, 15)

    def testTouchEvent2(self):
        """
        Adds touch event with set time and asserts session is in progress.
        Asserts session end time.
        """
        self.test_session.add_event(self.touch_1, 5)
        
        self.assertIsNotNone(self.test_session.session)
        self.assertEqual(self.test_session.session.end, 15)

    def testExpiredEvent(self):
        """
        Adds event after previous session has expired and asserts that previous
        session not in progress. New session instantiated.
        """
        self.test_session.add_event(self.touch_1, 3)
        prev_session = self.test_session.session
        
        self.test_session.add_event(self.touch_2, 15)

        self.assertNotEqual(prev_session, self.test_session.session)

    def testOverlappingTouches1(self):
        """
        Adds two overlapping touch events,
        with the second event ending after the first.
        """

        self.test_session.add_event(self.touch_1, 4)
        self.test_session.add_event(self.touch_2, 9)

        self.assertEqual(self.test_session.session.start, 4)
        self.assertEqual(self.test_session.session.end, 14)

    def testOverlappingTouches2(self):
        """
        Adds two overlapping touch events,
        with the second event ending before the first.
        """
        self.test_session.add_event(self.touch_1, 4)
        self.test_session.add_event(self.touch_2, 5)

        self.assertEqual(self.test_session.session.start, 4)
        self.assertEqual(self.test_session.session.end, 14)

    def testCheckOpenClose(self):
        """
        Adds check open event, asserts that check closes at -1
        until check close event happens.
        """
        
        self.test_session.add_event(self.check_open, 0)
        open_session = self.test_session.session

        self.assertIsNotNone(self.test_session.session)
        self.assertEqual(self.test_session.session.end, -1)

        self.test_session.add_event(self.check_close, 6)

        self.assertEqual(self.test_session.session.end, 6)
        self.assertEqual(open_session, self.test_session.session)


if __name__ == '__main__':
    unittest.main()
