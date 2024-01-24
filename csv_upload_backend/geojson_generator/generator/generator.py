
import geojson
from .supabase_client.client import SupabaseClient
from .utils.singleton_class import Singleton
from .data_classes.feature_models import PointFeature, LineStringFeature

class GeneratorBase:
    """ Parse DB entries and generate GeoJSON files and corresponding data entries """
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
                point_item = PointFeature(record, ind)
                self._points.append(point_item)

            if len(ind_records) > 1:
                line_item = LineStringFeature(ind_records, ind)
                self._lines.append(line_item)

    def get_points(self):
        """ Points getter """
        return self._points

    def get_lines(self):
        """ Lines getter """
        return self._lines

    def get_individuals(self):
        """ Individuals getter """
        return self._individuals

    def write_files(self, file_prefix: str):
        """ Create GeoJSON files in the parent directory

        Args:
            file_prefix (string): Identifier to append to the file name
        """
        for point in self._points:
            counter = 1
            filename = file_prefix + "_" + "point" + "_" + str(counter) + "_" + str(point.individual_id) + ".json"
            with open(filename, 'w',encoding="utf-8") as f:
                f.write(geojson.dumps(point.geoJSON))
                f.close()

        for line in self._lines:
            counter = 1
            filename2 = file_prefix + "_" + "line" + "_" + str(counter) + "_" + str(line.individual_id) + ".json"
            with open(filename2, 'w',encoding="utf-8") as f:
                f.write(geojson.dumps(line.geoJSON))
                f.close()

    def upload_files(self):
        """ Upload entries with GeoJSON data to the DB """
        for point in self._points:
            self._client.upsert_point(point)


class Generator(GeneratorBase, metaclass=Singleton):
    """ Singleton Class for the generator """

generator = Generator()
