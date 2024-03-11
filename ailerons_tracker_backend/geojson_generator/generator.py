""" Transfrom database entries into geoJSON files """
import json
import logging
from datetime import datetime
import geojson
import python_mts.scripts.mts_handler as mts
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.errors import GeneratorLineError, GeneratorPointError, GeoJSONFileWriteError, CreateRecipeError
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

    def update(self):
        """ Complete job: 
        - generate geojson data 
        - insert in db 
        - write geojson files, upload as sources
        - update tileset recipe
        - create and publish new TS from recipe 

        Raises:
            e: _description_
        """
        self.generate_geojson()

        self.upload_geojson()

        recipe = {
            "version": 1,
        }

        layers = {}

        for line in self._lines:
            filename = self.write_geojson_file(line)
            src_id = filename.strip(".json")

            try:
                self.handler.upload_source(src_id, filename, True)

                src_id = self.handler.get_source(src_id).json()['id']
                layer = {"source": src_id, "minzoom": 4, "maxzoom": 8}
                layers[line.individual_id] = layer

            except Exception as e:
                raise e

        recipe["layers"] = layers

        self.write_recipe(recipe)

        self.publish_new_ts()

    def generate_geojson(self):
        """ Generate GeoJSON features from fetched data

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

    def write_geojson_file(self, line: LineStringFeature):
        """ Create or update a geoJSON file

        Args:
            line (LineStringFeature)

        Returns:
            filename (str): name of the geoJSON file
        """
        try:
            filename = "line" + "_" + str(line.individual_id) + ".json"

            with open(filename, 'w', encoding="utf-8") as f:
                f.seek(0)
                f.write(geojson.dumps(line.geojson))
                f.truncate()
                f.close()

            return filename
        except Exception as e:
            raise GeoJSONFileWriteError(e) from e

    def write_recipe(self, recipe: dict, rcp_file_name: str = None):
        """ Create or update a recipe json file

        Args:
            recipe (dict): recipe data.
        """

        if not rcp_file_name:
            rcp_file_name = "recipe.json"

        try:
            with open(rcp_file_name, mode="w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(recipe))
                f.truncate()
                f.close()

        except Exception as e:
            raise CreateRecipeError(e) from e

    def publish_new_ts(self):
        """ Create and publish a new tileset through MTS Client """

        ts_name = datetime.today().strftime('%d-%m-%Y')

        self.handler.create_ts(
            ts_name, ts_name, recipe_path="recipe.json", private=True)

        r = self.handler.publish_ts(ts_name)
        logging.info(r.json())

    def upload_geojson(self):
        """ Upload entries with GeoJSON data to the DB """

        for col in self._points_collections:
            supabase.upsert(col, 'point_geojson')

        for line in self._lines:
            line.upload()


class Generator(GeneratorBase, metaclass=Singleton):
    """ Singleton Class for the generator """
