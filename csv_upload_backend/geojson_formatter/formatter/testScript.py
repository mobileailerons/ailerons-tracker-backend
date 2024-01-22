import dotenv
import os
from geojsonGenerator import generator
# from tilesetsJobs import tsHandler
from python_mts.scripts.mts_handler import Mts_Handler

dotenv.load_dotenv()

points = generator.get_points()
lines = generator.get_lines()

generator.write_files("test")

handler = Mts_Handler()

# handler.estimate_area("../../../test_line_1_2.json", "10m")
handler.list_sources()
print(lines)
