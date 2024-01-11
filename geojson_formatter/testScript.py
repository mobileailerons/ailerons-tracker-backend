from geojsonGenerator import generator


points = generator.get_points()
lines = generator.get_lines()

generator.write_files("test")