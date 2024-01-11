class Properties:
    def __init__(self, individual):
        self.individual_id = individual["id"]
        self.ind_common_name = individual["common_name"]
        self.ind_name = individual["individual_name"]
        self.icon = individual["icon"]

class PointProperties:
    def __init__(self, record, individual):
        Properties.__init__(self, individual)
        self.timestamp = record["record_timestamp"]

class LineProperties:
    def __init__(self, records, individual):
        Properties.__init__(self, individual)
        self.timestamp = list(map(lambda record : record["record_timestamp"], records))