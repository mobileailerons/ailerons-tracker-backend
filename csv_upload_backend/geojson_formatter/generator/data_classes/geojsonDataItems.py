from .properties import PointProperties, LineProperties
from geojson import Feature, Point, LineString

class PointDataItem:
    def __init__(self, record, individual):
        self.record_id = record["id"]
        self.csv_id = record["csv_id"]
        self.individual_id = individual["id"]
        self.geoJSON = self.__toPointFeature(record, individual)

    @staticmethod
    def __toPointFeature(record, individual):
        props = PointProperties(record, individual)
        geoJSON = Feature(geometry = Point((record["longitude"], record["latitude"])), properties = props.__dict__)

        if geoJSON.is_valid: return geoJSON
        else: print(geoJSON.errors())

class LineDataItem:
    def __init__(self, records, individual):
        self.record_ids = map(lambda record : record["id"], records)
        self.csv_ids = map(lambda record : record["csv_id"], records)
        self.individual_id = individual["id"]
        self.geoJSON = self.__toLineFeature(records, individual)

    @staticmethod
    def __toLineFeature(ind_records, individual):
        props = LineProperties(ind_records, individual)
        coordinates = list(map(lambda record : (record["longitude"], record["latitude"]), ind_records))
        geoJSON = Feature(geometry = LineString(coordinates), properties = props.__dict__ )
    
        if geoJSON.is_valid: return geoJSON
        else: print(geoJSON.errors())