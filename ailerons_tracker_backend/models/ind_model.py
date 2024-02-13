""" Individual and Context models """
from ailerons_tracker_backend.clients.supabase_client import supabase


class Individual:
    """ Model for an individual """

    def __init__(self, form, image_urls: list[str]):
        self.name: str = form['indName']
        self.sex: str = form['indSex']
        self.pictures = image_urls

    def upload(self):
        """ Insert the object as a new row in table 'individual' """

        data = supabase.upsert(self, 'individual')
        return data


class Context:
    """ Model for an individual's tagging context """

    def __init__(self, ind_id, form):
        self.date = form['date']
        self.individual_id: int = ind_id
        self.situation: str = form['situation']
        self.size: int = form['indSize']
        self.mature: bool = form['mature']
        self.feeding: bool = form['feeding']
        self.reproduction: bool = form['reproduction']
        self.gestation: bool = form['gestation']
        self.jumping: bool = form['jumping']
        self.injured: bool = form['injured']
        self.sick: bool = form['sick']
        self.parasites: bool = form['parasites']

    def upload(self):
        """ Insert the object as a new row in table 'context' """

        data = supabase.upsert(self, 'context')
        return data
