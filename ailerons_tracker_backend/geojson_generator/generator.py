""" Transfrom database entries into geoJSON files """
import json
import logging
import os
import geojson
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.errors import GeneratorLineError, GeneratorPointError
from ailerons_tracker_backend.utils.singleton_class import Singleton
from .data_classes.feature_models import PointFeature, LineStringFeature
import python_mts.scripts.mts_handler as mts


class GeneratorBase:
    """ Parse DB entries and generate GeoJSON files and corresponding data entries """

    def __init__(self):
        # récupère la liste des individus depuis la BDD
        self._individuals = supabase.get_all('individual')
        self._points: list[list[PointFeature]] = []
        self._lines: list[LineStringFeature] = []
        self._points_collections: list[geojson.FeatureCollection] = []
        self.handler = mts.MtsHandler()

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

        self.__upload_files()
        self.__write_files("test")

    def __write_files(self, file_prefix: str):
        """ Create GeoJSON files in the parent directory

        Args:
            file_prefix (string): Identifier to append to the file name
        """

        for line in self._lines:
            counter = 1
            filename2 = file_prefix + "_" + "line" + "_" + \
                str(counter) + "_" + str(line.individual_id) + ".json"

            with open(filename2, 'w', encoding="utf-8") as f:
                f.write(geojson.dumps(line.geojson))
                f.close()

                try:
                    self.__publish_new_ts(filename2)
                except Exception as e:
                    raise e

    def __publish_new_ts(self, filename: str):
        self.handler.upload_source("test", filename, True)

        source_url = self.handler.get_source("test").json()['id']
        logging.info(source_url)
        test_recipe: dict = {"version": 1,
                             "layers": {
                                 "trees": {
                                     "source": source_url,
                                     "minzoom": 4,
                                     "maxzoom": 8
                                 }
                             }
                             }
        
        with open("test_recipe.json", mode="w", encoding="utf-8") as f:
            f.write(json.dumps(test_recipe))
            f.close()

        self.handler.create_ts(
            "test", "test", recipe_path="test_recipe.json", private=True)
        r = self.handler.publish_ts("test")
        logging.info(r.json())

    def __upload_files(self):
        """ Upload entries with GeoJSON data to the DB """
        logging.debug("UPLOADING")
        for col in self._points_collections:
            supabase.upsert(col, 'point_geojson')

        for line in self._lines:
            line.upload()


class Generator(GeneratorBase, metaclass=Singleton):
    """ Singleton Class for the generator """
