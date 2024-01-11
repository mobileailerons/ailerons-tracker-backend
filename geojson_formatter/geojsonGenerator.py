
import geojson
from supabaseClient import SupabaseClient
from singletonClass import Singleton
from geojsonDataItems import PointDataItem, LineDataItem

class GeneratorBase:
    def __init__(self):
        self._client = SupabaseClient()
        self._individuals = self._client.get_individuals()
        self._points = []
        self._lines = []
    
        for ind in self._individuals:
            ind_records = self._client.get_ind_records(ind["id"])
            for record in ind_records:
                pointItem = PointDataItem(record, ind)
                self._points.append(pointItem)

            if len(ind_records) > 2:
                lineItem = LineDataItem(ind_records, ind)
                self._lines.append(lineItem)
                
    def get_points(self):
        return self._points
    
    def get_lines(self):
        return self._lines
    
    def get_individuals(self):
        return self._individuals

    def write_files(self, filePrefix):
        for point in self._points:
            counter = 1
            filename = "./" + filePrefix + "_" + "point" + "_" + str(counter) + "_" + str(point.individual_id) + ".geojson"
            with open(filename, 'w') as f:
                f.write(geojson.dumps(point.geoJSON))
                f.close()

        for line in self._lines:
            counter = 1
            filename2 = "./" +filePrefix + "_" +"line" + "_" + str(counter) + "_" + str(line.individual_id) + ".geojson"
            with open(filename2, 'w') as f:
                f.write(geojson.dumps(line.geoJSON))
                f.close()

class Generator(GeneratorBase, metaclass=Singleton):
    pass

generator = Generator()