""" File model """

class File:
    """ Model for a CSV file. """

    def __init__(self, file_path, file_db_id):
        self.path = file_path
        self.db_id = file_db_id
