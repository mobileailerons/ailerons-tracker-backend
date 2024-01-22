import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self._url: str = os.getenv("SUPABASE_URL")
        self._key: str = os.getenv("SUPABASE_KEY")
        self._client: Client = create_client(self._url, self._key)

    def get_individuals(self):
        res = self._client.table("individual").select("*").execute()
        return res.data
    def get_ind_records(self, individual_id):
        res = self._client.table("record").select("*").eq("individual_id", individual_id).execute()
        return res.data

    def postPoints(self, pointData):
        data = self._client.table('point_geojson').upsert({"csv_id": pointData.csv_id, "record_id": pointData.record_id, "individual_id": pointData.individual_id, "geojson": pointData.geoJSON}).execute()
        print(data)
