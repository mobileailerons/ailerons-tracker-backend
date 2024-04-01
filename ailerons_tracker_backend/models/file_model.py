""" File model """

class File:
    """ Model for a CSV file. """

    def __init__(self, file_informations):
        self.path = file_informations.file_path
        self.db_id = file_informations.file_db_id
