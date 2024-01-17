import os
import sys
import subprocess
from singletonClass import Singleton
from dotenv import load_dotenv

load_dotenv()

class TilesetsHandlerBase:
    def __init__(self):
        self._mapboxToken = os.getenv("MAPBOX_ACCESS_TOKEN")
        self._username = os.getenv("MAPBOX_USER_NAME")
        self._cwd = os.path.dirname(os.path.realpath(__file__))


    def createSource(self, source_name, source_path):
        estimate = self.estimateArea(source_path)
        # result = subprocess.run([sys.executable, ".venv/bin/tilesets", "upload-source", self._username, source_name, source_path], capture_output=True, timeout=10)
        # print("out:", result.stdout)
        # print("err:", result.stderr)

    def getHelp(self):
        result = subprocess.run([sys.executable, ".venv/bin/tilesets", "--help"], capture_output=True, timeout=15)
        print("out:", result.stdout)
        print("err:", result.stderr)

        

    def listSources(self):
        result = subprocess.run( [ sys.executable, ".venv/bin/tilesets", "list-sources", self._username], capture_output=True, timeout=5)
        print("out:", result.stdout)
        print("err:", result.stderr)
    
    def estimateArea(self, feature):
        precision = '10m'
        result = subprocess.run( [ sys.executable, ".venv/bin/tilesets", "estimate-area", "-p", precision,], capture_output=True, timeout=20)
        print("out:", result.stdout)
        print("err:", result.stderr)
        return result.stdout

        
class TilesetsHandler(TilesetsHandlerBase, metaclass=Singleton):
    pass

tsHandler = TilesetsHandler()