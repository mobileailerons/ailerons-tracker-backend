from geojsonGenerator import generator


points = generator.get_points()
lines = generator.get_lines()

generator.upload_files()