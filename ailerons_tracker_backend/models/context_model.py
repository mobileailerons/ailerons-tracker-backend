""" Context model """
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.errors import UpdateError


class Context:
    """ Model for an individual's tagging context.

        Properties:
            tag_date (DateTime): Date of tagging.
            individual_id (int): Primary key of matching Individual.
            situation (str): Wether the individual was alone, part of a group or with its reproductive partner.
            size (int): Measured span of the Individual when tagged.
            behavior (str): Observed behavior.
            id (int): Primary key of DB row. """

    def __init__(self, individual_id: int, date: str, situation: str, size: int, behavior: str, context_id: int | None = None):
        self._date: str = date
        self._individual_id: int = individual_id
        self._situation: str = situation
        self._size: int = size
        self._behavior: str = behavior
        self._id: int|None = context_id

    @property
    def date(self):
        """ tag date getter """
        return self._date

    @property
    def individual_id(self):
        """ associated individual ID getter """
        return self._individual_id

    @property
    def situation(self):
        """ situation getter """
        return self._situation

    @situation.setter
    def situation(self, new_situation: str):
        if new_situation != self._situation and new_situation in ["alone", "group", "couple"]:
            self._situation = new_situation

    @property
    def size(self):
        """ size when tagged getter """
        return self._size

    @size.setter
    def size(self, new_size: str):
        if not new_size == self._size and new_size < 20:
            self._size = new_size

    @property
    def behavior(self):
        """ behavior when tagged getter """
        return self._behavior

    @behavior.setter
    def behavior(self, new_behavior):
        if new_behavior != self._behavior:
            self._behavior = new_behavior

    @property
    def id(self):
        """ ID getter """
        return self._id

    @id.setter
    def id(self, new_id):
        if not self._id:
            self._id = new_id

    @classmethod
    def get_from_db(cls, context_id: int | str):
        """ Get context data from DB and instanciate a model """

        row = supabase.get_exact('id', context_id, 'context')

        return Context(
            context_id=context_id,
            date=row.get("date"),
            situation=row.get("situation"),
            size=row.get("size"),
            behavior=row.get("behavior"),
            individual_id=row.get("individual_id")
        )

    def to_dict(self):
        """ Return instance attributes and class variables as a dict """

        context_dict = {
            'date': self._date,
            'situation': self._situation,
            'size': self._size,
            'behavior': self._behavior
        }

        if self._id:
            context_dict['id'] = self._id

        return context_dict

    @classmethod
    def get_with_ind_id(cls, individual_id):
        """ Get context data with corresponding individual ID """

        row = supabase.get_exact('individual_id', individual_id, 'context')

        return Context(individual_id=individual_id,
                       date=row.get("date"),
                       situation=row.get("situation"),
                       size=row.get("size"),
                       behavior=row.get("behavior"),
                       context_id=row.get("context_id"))

    def update(self, **updates):
        """ Update model through setters """

        try:
            self.size = updates.get("size", self.size)
            self.situation = updates.get("sex", self.situation)
            self.behavior = updates.get("behavior", self.behavior)

        except Exception as e:
            raise UpdateError(e) from e

    def upload(self):
        """ Insert the object as a new row in table 'context' """

        data = supabase.upsert(self.to_dict(), 'individual')
        self.id = data[0].get("id")
        return data
