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

    def get_individual_ids(self):
        """ Get all individual_ids from join table """

        res = self._client.table('individual_record_id').select(
            "individual_id").execute()

        return res.data

    def get_all(self, table: str):
        """ Get every row from a specific table """

        res = self._client.table(table).select("*").execute()
        return res.data

    def get_match(self, col: str, matcher: str, table: str):
        """ Get every row from table where column value matches the provided value """

        res = self._client.table(table).select(
            "*").eq(col, matcher).execute()
        return res.data

    def upsert_feature(self, table: str, obj: object):
        """ Insert or update a row in table 'point_geojson' """
        if not table == ("point_geojson" or "line_geojson"):
            raise TypeError(table)

        data = self._client.table(table).upsert(
            obj.__dict__).execute()

        return data.__dict__

    def upsert_article(self, article: object):
        """ Insert or update a row in table 'article' """
        data = self._client.table("article").upsert(
            article.__dict__).execute()

        return data.__dict__

    def create_csv_log(self, file_name: str):
        """ Create and insert a CSV log in the DB and returns the generated ID """
        csv_log = {'file_name': file_name}
        data = self._client.table('csv').insert(csv_log).execute()
        content = data.__dict__.get('data')[0]

        return content.get("id")

    def batch_insert(self, table: str, datalist: list):
        """ Batch insert new rows in table Record """

        data = self._client.table(table).insert(datalist).execute()

        return data.__dict__


supabase = SupabaseClient()
