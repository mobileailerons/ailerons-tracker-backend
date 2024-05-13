""" GeoJSON properties Data Classes """


class Properties:
    """ Properties Base Class """

    def __init__(self, individual):
        self.individual_id = individual["id"]
        self.ind_name = individual["individual_name"]
        self.pictures = individual["picture"]


class PointProperties(Properties):
    """ Point Feature properties """

    def __init__(self, record, individual):
        Properties.__init__(self, individual)
        self.timestamp = record["record_timestamp"]


class LineProperties(Properties):
    """ Linestring Feature Properties """

    def __init__(self, records, individual):
        Properties.__init__(self, individual)
        self.timestamp = list(
            map(lambda record: record["record_timestamp"], records))
