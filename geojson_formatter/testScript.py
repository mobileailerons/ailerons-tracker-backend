from geojsonGenerator import generator
from tilesetsJobs import tsHandler

points = generator.get_points()
lines = generator.get_lines()

# generator.write_files("test")

tsHandler.createSource("test-2","./test_point_1_3.json")