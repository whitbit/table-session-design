import operator
from uuid import uuid4
from datetime import datetime

class Session(object):

    def __init__(self, sesh_id, start, end):
        self.id = sesh_id
        self.start = start
        self.end = end


class Event(object):

    event_types = ['check_open', 'check_close', 'swipe', 'touch']

    def __init__(self, name, timeout=-1):
        self.name = name
        self.timeout = timeout

    name = property(operator.attrgetter('_name'))

    @name.setter
    def name(self, name):
        if name not in self.event_types:
            raise Exception('Not a valid event.')
        else:
            self._name = name


class SessionController(object):

    def __init__(self):
        self.session = None
        self.all_sessions = []


    def add_event(self, event, timestamp):
        """
        Instantiates new session and returns True if creating a new session.
        Or extends session and returns False.

        """

        new_event_end = timestamp + event.timeout

        is_created = False

        if self.session \
           and (self.session.end > timestamp or self.session.end == -1):
            if event.name == 'check_close':
                self.session.end = timestamp
            if event.name == 'check_open':
                self.session.end = -1
            if (self.session.end > timestamp
                and self.session.end < new_event_end):
                self.session.end = new_event_end
            return is_created

        is_created = True

        self.session = Session(uuid4(), timestamp, new_event_end)
        self.all_sessions.append(self.session)
        
        return is_created


    def get_current_session(self):
        """
        If there is a session, returns session object. If not,
        returns None.
        """
        if self.session is not None:
            return self.session
        else:
            return None

    def get_sessions(self):
        """
        Returns list of historic sessions.

        """

        return self.all_sessions
