import unittest
from controller import Session, Event, SessionController


class SessionTestCase(unittest.TestCase):

    def setUp(self):
        self.test_session = SessionController()
        self.touch_1 = Event('touch', 10)
        self.touch_2 = Event('touch', 5)
        self.check_open = Event('check_open')
        self.check_close = Event('check_close')

    def testTouchEvent(self):
        """
        Submits touch event and asserts session is in progress.
        """
        
        self.assertEqual(self.test_session.add_event(self.touch_1, 5), True)
        self.assertIsNotNone(self.test_session.get_current_session())

    def testOverlappingTouches(self):
        """
        Submits two overlapping touch events,
        with the second event ending after the first.
        """

        self.test_session.add_event(self.touch_1, 4)
        self.test_session.add_event(self.touch_2, 9)

        self.assertEqual(self.test_session.session.session_start, 4)
        self.assertEqual(self.test_session.session.session_end, 14)

    def testOverlappingTouches2(self):
        """
        Submits two overlapping touch events,
        with the second event ending before the first.
        """

        self.test_session.add_event(self.touch_1, 4)
        self.test_session.add_event(self.touch_2, 5)

        self.assertEqual(self.test_session.session.session_start, 4)
        self.assertEqual(self.test_session.session.session_end, 10)

    def testCheckOpenCheckClose(self):
        """
        Opens a session with check_open. Wait for long time.
        """
        self.test_session.add_event(self.check_open, 19)
        
        # checks current session id after opening a check
        session_id = self.test_session.session.session_id

        # checks that current session ends at infinite time
        self.assertEqual(self.test_session.session.session_end, -1)

        # closes session with check close and checks that it's the same previous session
        # self.test_session.add_event(self.check_close, 100)
        # self.assertEqual(self.test_session.session.session_end, 100)
        # self.assertEqual(self.test_session.session.session_id, session_id)  


if __name__ == '__main__':
    unittest.main()
