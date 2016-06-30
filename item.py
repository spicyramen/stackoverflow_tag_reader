class Item(object):
    def __init__(self):
        self._id = None
        self._link = None
        self._tags = None
        self._body = None
        self._body_clean = None
        self._answer_count = None
        self._is_answered = False
        self._answers = list()  # Each question has one or more associated answer. Store as a list of objects
        self._text = None
        self._title = None

    @property
    def id(self):
        """I'm the question Id property."""
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def link(self):
        """I'm the question URL property."""
        return self._link

    @link.setter
    def link(self, link):
        self._link = link

    @property
    def answer_count(self):
        """I'm the question URL property."""
        return self._answer_count

    @answer_count.setter
    def answer_count(self, answer_count):
        self._answer_count = answer_count

    @property
    def is_answered(self):
        """Contains an answer"""
        return self._is_answered

    @is_answered.setter
    def is_answered(self, is_answered):
        self._is_answered = is_answered

    @property
    def tags(self):
        """I'm the question Tags property."""
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    @property
    def answers(self):
        """I'm the question Id property."""
        return self._answers

    @answers.setter
    def answers(self, answers):
        self._answers = answers

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
    def text(self):
        """
        :return:
        """
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def title(self):
        """I'm the question URL property."""
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    def __str__(self):
        return self._text

    def __repr__(self):
        return self._text