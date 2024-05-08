""" Individual and Context models """
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.errors import UpdateError


class Individual:
    """ Model for an individual """

    common_name: str = 'Diable de mer méditerranéen'
    binomial_name: str = 'Mobula mobular'
    icon: str = 'https://static.thenounproject.com/png/1469351-200.png'

    def __init__(self, name: str, sex: str, pictures: list[str], description: str = '', individual_id=None):
        self._name: str = name
        self._sex: str = sex
        self._pictures: list[str] = pictures
        self._description: str = description
        self._id = individual_id

    @property
    def name(self):
        """ name getter """
        return self._name

    @name.setter
    def name(self, new_name: str):
        if not new_name == self._name:
            self._name = new_name

    @property
    def sex(self):
        """ sex getter """
        return self._sex

    @sex.setter
    def sex(self, new_sex: str):
        if new_sex in ['Male', 'Femelle', 'Inconnu'] and new_sex != self._sex:
            self._sex = new_sex

    @property
    def pictures(self):
        """ pictures getter """
        return self._pictures

    @pictures.setter
    def pictures(self, new_pics: list[str]):
        for pic in new_pics:
            if not pic in self._pictures:
                self._pictures.append(pic)

    @pictures.deleter
    def pictures(self):
        del self.pictures

    @property
    def description(self):
        """ desc getter """
        return self._description

    @description.setter
    def description(self, new_desc: str):
        if not new_desc == self._description:
            self._description = new_desc

    @property
    def id(self):
        """ ID getter """
        return self._id

    @id.setter
    def id(self, new_id):
        if not self._id:
            self._id = new_id

    @classmethod
    def get_from_db(cls, individual_id):
        """ Get an individual's data from DB and instanciate a model """

        row = supabase.get_exact('id', individual_id, 'individual_new')

        return Individual(
            individual_id=individual_id,
            name=row["name"],
            sex=row["sex"],
            pictures=row["pictures"],
            description=row["description"])

    def to_dict(self):
        """ Return instance attributes and class variables as a dict """

        ind_dict = {'name': self._name,
                    'sex': self._sex,
                    'pictures': self._pictures,
                    'description': self._description,
                    'common_name': Individual.common_name,
                    'binomial_name': Individual.binomial_name,
                    'icon': Individual.icon}

        if self._id:
            ind_dict['id'] = self._id

        return ind_dict

    def update(self, **updates):
        """ Update model through setters """

        try:
            self.name = updates.get("name", self.name)
            self.sex = updates.get("sex", self.sex)
            self.description = updates.get("description", self.description)
            self.pictures = updates.get("pictures", self.pictures)

        except Exception as e:
            raise UpdateError(e) from e

    def upload(self):
        """ Insert the object as a new row in table 'context' """

        data = supabase.upsert(self.to_dict(), 'individual_new')
        self.id = data[0].get("id")
        return data
