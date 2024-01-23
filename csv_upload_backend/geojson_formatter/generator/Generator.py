
import geojson
from .supabase_client.supabaseClient import SupabaseClient
from .utils.singletonClass import Singleton
from .data_classes.geojsonDataItems import PointDataItem, LineDataItem

class GeneratorBase:
    def __init__(self):
        self._client = SupabaseClient()
        # récupère la liste des individus depuis la BDD
        self._individuals = self._client.get_individuals()
        self._points = []
        self._lines = []

        # récupère les relevés pour chaque individu
        for ind in self._individuals:
            ind_records = self._client.get_ind_records(ind["id"])
            # crée un objet
            for record in ind_records:
                pointItem = PointDataItem(record, ind)
                self._points.append(pointItem)

            if len(ind_records) > 1:
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
            filename = filePrefix + "_" + "point" + "_" + str(counter) + "_" + str(point.individual_id) + ".json"
            with open(filename, 'w',encoding="utf-8") as f:
                f.write(geojson.dumps(point.geoJSON))
                f.close()

        for line in self._lines:
            counter = 1
            filename2 = filePrefix + "_" + "line" + "_" + str(counter) + "_" + str(line.individual_id) + ".json"
            with open(filename2, 'w',encoding="utf-8") as f:
                f.write(geojson.dumps(line.geoJSON))
                f.close()

    def upload_files(self):
        for point in self._points:
            self._client.postPoints(point)


class Generator(GeneratorBase, metaclass=Singleton):
    pass

generator = Generator()