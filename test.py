import unittest
from controller import Session, Event, SessionController


class SessionTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = SessionController()
        cls.touch = Event('touch', 10)

    def testTouchEvent(self):
        # session = SessionController()
        # touch = Event('touch', 10)
        
        self.assertEqual(self.session.add_event(self.touch, 10), True)
        self.assertIsNotNone(self.session.get_current_session())
        self.assertEqual(self.session.get_current_session(), self.session)

    
# test_session = SessionController()
# open_check = Event('check_open', -1)
# swipe = Event('swipe', 5)
# touch = Event('touch', 10)
# close = Event('check_close')

if __name__ == '__main__':
    unittest.main()
