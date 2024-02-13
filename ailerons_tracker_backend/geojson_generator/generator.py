""" Transfrom database entries into geoJSON files """
import logging
import geojson
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.errors import GeneratorLineError, GeneratorPointError
from ailerons_tracker_backend.utils.singleton_class import Singleton
from .data_classes.feature_models import PointFeature, LineStringFeature


class GeneratorBase:
    """ Parse DB entries and generate GeoJSON files and corresponding data entries """

    def __init__(self):
        # récupère la liste des individus depuis la BDD
        self._individuals = supabase.get_all('individual')
        self._points: list[list[PointFeature]] = []
        self._lines: list[LineStringFeature] = []
        self._points_collections: list[geojson.FeatureCollection] = []

    def get_points(self):
        """ Points getter """
        return self._points

    def get_lines(self):
        """ Lines getter """
        return self._lines

    def get_p_collections(self):
        """ Collections getter """
        return self._points_collections

    def get_individuals(self):
        """ Individuals getter """
        return self._individuals

    def generate(self):
        """ Generate GeoJSON objects from fetched data

        Raises:
            GeneratorPointError: Error generating Point Features
            GeneratorLineError: Error generating LineString Features
        """

        for ind in self._individuals:
            ind_records = supabase.get_match(
                "individual_id", ind["id"], "record")

            ind_points = []
            try:
                for record in ind_records:
                    point_item = PointFeature(record, ind)
                    ind_points.append(point_item)

            except Exception as e:
                raise GeneratorPointError from e

            if len(ind_records) > 1:
                try:
                    line_item = LineStringFeature(ind_records, ind)
                    self._lines.append(line_item)

                except Exception as e:
                    raise GeneratorLineError from e

            self._points.append(ind_points)
            self._points_collections.append(
                geojson.FeatureCollection(ind_points))

    def write_files(self, file_prefix: str):
        """ Create GeoJSON files in the parent directory

        Args:
            file_prefix (string): Identifier to append to the file name
        """

        for point in self._points:
            counter = 1
            filename = file_prefix + "_" + "point" + "_" + \
                str(counter) + "_" + str(point.individual_id) + ".json"

            with open(filename, 'w', encoding="utf-8") as f:
                f.write(geojson.dumps(point.geoJSON))
                f.close()

        for line in self._lines:
            counter = 1
            filename2 = file_prefix + "_" + "line" + "_" + \
                str(counter) + "_" + str(line.individual_id) + ".json"

            with open(filename2, 'w', encoding="utf-8") as f:
                f.write(geojson.dumps(line.geoJSON))
                f.close()

    def upload_files(self):
        """ Upload entries with GeoJSON data to the DB """
        logging.debug("UPLOADING")
        for col in self._points_collections:
            supabase.upsert(col, 'point_geojson')

        for line in self._lines:
            line.upload()


class Generator(GeneratorBase, metaclass=Singleton):
    """ Singleton Class for the generator """
