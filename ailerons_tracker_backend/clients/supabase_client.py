""" Supabase Python Client """

import os
from dotenv import load_dotenv
from supabase import create_client, Client
import uuid

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

    def upsert(self, obj: object, table: str):
        """ Insert or update a row in selected table """

        data = self._client.table(table).upsert(
            obj.__dict__).execute()

        return data.__dict__

    def create_csv_log(self, uuid: str, loc_file_name: str, depth_file_name: str):
        """ Create and insert a CSV log in the DB and returns the generated ID """
        csv_id = uuid.uuid4()
        csv_log = { 'uuid': uuid,
                   'loc_file': loc_file_name,
                    'depth_file': depth_file_name }
        data = self._client.table('csv').insert(csv_log).execute()
        content = data.__dict__.get('data')[0]

        return content.get("id")

    def batch_insert(self, table: str, datalist: list):
        """ Batch insert new rows in table Record """

        data = self._client.table(table).insert(datalist).execute()

        return data.__dict__


supabase = SupabaseClient()
