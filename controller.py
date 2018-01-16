import operator

class Session(object):

    def __init__(self, session_start, session_end):
        self.session_start = session_start
        self.session_end = session_end

class Event(object):

    event_types = ['check_open', 'check_close', 'swipe', 'touch']

    def __init__(self, name, *timeout):
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

        #Handles new session cases if no session exists or if session expired.
        
        if self.session == None or self.session.session_end < timestamp:
            if event.name == 'check-open':
                self.session = Session(timestamp, -1)
            if event.name == 'swipe' or event.name == 'touch':
                self.session = Session(timestamp, event.timeout)
            
            self.all_sessions.append(self.session)
            
            return True

        """
        Handles extending session with check-open.
        """
        if event.name == 'check_open':
            self.session.session_end = -1


        # Handles extending session if session is not in check open state
        # and new event timeout is later than existing session timeout.
        if (self.session.session_end is not -1) \
            and (self.session.session_end < timestamp + event.timeout):
            self.session.session_end = timestamp + event.timeout
        
        if event.name == 'check_close':
            self.session.session_end = timestamp

        return False
        

    def get_current_session(self):
        """
        If there is a session, returns session object. If not,
        returns None.
        """
        if self.session is not None:
            return self.session
        else:
            return None

    def get_all_sessions(self):
        """
        Returns list of historic sessions.

        """

        return self.all_sessions
