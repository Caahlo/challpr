import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

import s2_py as s2

def geopackage_to_text(input_path, output_path):
    layer=gpd.read_file(input_path)
    length=layer.grade.size
    text=open(output_path,"w+")
    for i in range(length):
        text.write(str(layer.geometry[i])+"\n")
    text.close()
    print("converted gpkg to txt")

def process_multipolygon(input_path, output_path):
    text_in=open(input_path,"r")
    text_out=open(output_path,"w+")
    textdata=text_in.readlines()
    counter=0
    n_of_points=0
    for line in textdata:
        counter+=1
        line= line[16:-4]
        points=line.split(",")
        text_out.write("Polygon"+str(counter)+"\n")
        for point in points:
            n_of_points+=1
            text_out.write(point+"\n")
        text_out.write("\n")
    print(n_of_points)
    print("spilt the stuff up into points")

def process_points(input_path,output_path):
    print("splittin' it up into coordinates")
    text_in=open(input_path,"r")
    text_out=open(output_path,"w+")
    textdata=text_in.readlines()
    for line in textdata:
        coords=line.split(" ")
        for coord in coords:
            text_out.write(coord+"\n")
    print("split it up fam")

def text_to_points(input_path):
    text_in=opne(input_path,"r")
    

geopackage_to_text("/home/carlo/challpr/OeVGK_layers/json_Werktag_Tag.geojson","werktag_tag.txt")
process_multipolygon("werktag_tag.txt","werktag_tag_points.txt")
process_points("werktag_tag_points.txt","werktag_tag_coords.txt")