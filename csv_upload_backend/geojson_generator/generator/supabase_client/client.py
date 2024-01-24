""" Supabase Python Client """

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class SupabaseClient:
    """ Supabase Client wrapper with credentials """
    def __init__(self):
        self._url: str = os.getenv("SUPABASE_URL")
        self._key: str = os.getenv("SUPABASE_KEY")
        self._client: Client = create_client(self._url, self._key)

    def get_individuals(self):
        """ Get every row from table 'individual' """
        res = self._client.table("individual").select("*").execute()
        return res.data
    def get_ind_records(self, individual_id: str):
        """ Get every row from table 'record' that matches the given individual_id """
        res = self._client.table("record").select("*").eq("individual_id", individual_id).execute()
        return res.data

    def upsert_point(self, point_data):
        """ Insert or update a row in table 'point_geojson' """
        data = self._client.table('point_geojson').upsert(
            {"csv_id": point_data.csv_id,
            "record_id": point_data.record_id,
            "individual_id": point_data.individual_id,
            "geojson": point_data.geojson}).execute()
        return data.__dict__

    def upsert_line(self, line_data):
        """ Insert or update a row in table 'line_geojson' """
        data = self._client.table('line_geojson').upsert(
            {"csv_id": line_data.csv_id,
            "individual_id": line_data.individual_id,
            "geojson": line_data.geojson}).execute()
        return data.__dict__
