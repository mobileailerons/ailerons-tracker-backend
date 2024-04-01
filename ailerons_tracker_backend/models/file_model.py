""" File model """

class File:
    """ Model for a CSV file. """

    def __init__(self, file_informations):
        self.file_path = file_informations.file_path
        self.file_db_id = file_informations.file_db_id
