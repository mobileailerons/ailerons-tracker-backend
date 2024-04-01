""" Individual and Context models """
from ailerons_tracker_backend.clients.supabase_client import supabase


class Individual:
    """ Model for an individual """

    def __init__(self, name: str, sex: str, image_urls: list[str], description: str = ''):
        self.name: str = name
        self.sex: str = sex
        self.pictures = image_urls
        self.common_name: str = 'Diable de mer méditerranéen'
        self.binomial_name: str = 'Mobula mobular'
        self.description: str = description
        self.icon: str = 'https://www.flaticon.com/free-icon/manta-ray_2253552?term=manta+ray&page=1&position=9&origin=tag&related_id=2253552'

    def upload(self):
        """ Insert the object as a new row in table 'individual_new' """

        data = supabase.upsert(self, 'individual_new')
        return data


class Context:
    """ Model for an individual's tagging context """

    def __init__(self, individual_id: int, date: str, situation: str, size: int, behavior: str):
        self.date = date
        self.individual_id: int = individual_id
        self.situation: str = situation
        self.size: int = size
        self.behavior: str = behavior

    def upload(self):
        """ Insert the object as a new row in table 'context' """

        data = supabase.upsert(self, 'context')
        return data
