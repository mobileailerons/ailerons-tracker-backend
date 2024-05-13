""" Supabase Python Client """

import os
from dotenv import load_dotenv
from ailerons_tracker_backend.errors import EnvVarError
from supabase.client import create_client

load_dotenv()

sb_url = os.getenv("SUPABASE_URL")
sb_key = os.getenv("SUPABASE_KEY")


class SupabaseClient:
    """ Supabase Client wrapper with credentials """

    def __init__(self):

        if not sb_url:
            raise EnvVarError("SUPABASE_URL")
        else:
            self._url: str = sb_url

        if not sb_key:
            raise EnvVarError("SUPABASE_KEY")
        else:
            self._key: str = sb_key

        self._client = create_client(self._url, self._key)

    @property
    def client(self):
        return self._client

    def get_individual_ids(self) -> list[int]:
        """ Get all individual_ids from join table """

        res = self._client.table('individual').select(
            "id").execute()

        return [d['id'] for d in res.data]

    def get_all(self, table: str) -> list[dict]:
        """ Get every row from a specific table

        Args:
            table (str): table name.
        """

        res = self._client.table(table).select("*").execute()

        return res.data

    def get_match(self, matcher: str, value, table: str) -> list[dict]:
        """ Get every row from table where column value matches the provided value

        Args:
            matcher (str): column to match with.
            value: value to search for.
            table (str): table name.
        """

        res = self._client.table(table).select(
            "*").eq(matcher, value).execute()

        return res.data

    def get_exact(self, matcher: str, value, table: str) -> dict:
        """ Get specific row from table where primary key matches provided value

        Args:
            matcher (str): column to match with.
            value: value to search for.
            table (str): table name.
        """

        res = self._client.table(table).select(
            "*").eq(matcher, value).maybe_single().execute()

        if res:
            return res.data

        raise ValueError()

    def insert(self, row_data: dict, table: str) -> list[dict]:
        """ Insert or update a row in selected table

        Args:
            row_data (dict): data to upload.
            table (str): table name.
        """

        res = self._client.table(table).insert(
            row_data).execute()

        return res.data

    def update(self, matcher: str, value, row_data: dict, table: str) -> list[dict]:
        """ Insert or update a row in selected table

        Args:
            matcher (str): column to match with.
            value: value to search for.
            row_data (dict): data to upload.
            table (str): table name.
        """

        res = self._client.table(table).update(
            row_data).eq(matcher, value).execute()

        return res.data

    def upsert(self, row_data: dict, table: str) -> list[dict]:
        """ Insert or update a row in selected table

        Args:
            row_data (dict): data to upload.
            table (str): name of the table.
        """

        res = self._client.table(table).upsert(
            row_data).execute()

        return res.data

    def create_csv_log(self, uuid: str, loc_file_name: str, depth_file_name: str):
        """ Create and insert a CSV log in the DB and returns the generated ID """

        csv_log = {'uuid': uuid,
                   'loc_file': loc_file_name,
                   'depth_file': depth_file_name}

        data = self._client.table('csv').insert(csv_log).execute()
        content = data.__dict__.get('data')[0]
        return content

    def batch_insert(self, table: str, datalist: list[dict]):
        """ Batch insert new rows in table Record

        Args:
            table (str): table name.
            datalist (list): list of data dicts. 
        """

        res = self._client.table(table).insert(datalist).execute()

        return res.data


supabase = SupabaseClient()
