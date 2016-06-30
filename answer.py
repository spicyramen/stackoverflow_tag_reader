

class Answer(object):
    """

    """

    def __init__(self):
        self._id = None
        self._link = None
        self._tags = None
        self._is_accepted = False
        self._body = None
        self._body_clean = None

    @property
    def id(self):
        """I'm the answer Id property."""
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def body(self):
        """I'm the answer Body roperty."""
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def body_clean(self):
        """I'm the answer Body property."""
        return self._body_clean

    @body_clean.setter
    def body_clean(self, body_clean):
        self._body_clean = body_clean

    @property
    def link(self):
        """I'm the answer URL property."""
        return self._link

    @link.setter
    def link(self, link):
        self._link = link

    @property
    def is_accepted(self):
        """Contains an answer"""
        return self._is_accepted

    @is_accepted.setter
    def is_accepted(self, is_accepted):
        self._is_accepted = is_accepted

    def __str__(self):
        return self._body_clean

    def __repr__(self):
        return self._body_clean