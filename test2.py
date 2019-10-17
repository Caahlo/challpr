import geopandas as gpd
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import s2sphere as s2s

import s2_py as s2

def geopackage_to_text(input_path, output_path):
    layer=gpd.read_file(input_path)
    length=layer.grade.size
    text=open(output_path,"w+")
    for i in range(length):
        text.write(str(layer.geometry[i])+"\n")
    text.close()
    print("converted gpkg to txt")

def multipolygon_to_polygon(input_path, output_path):
    text_in=open(input_path,"r")
    text_out=open(output_path,"w+")
    textdata=text_in.readlines()
    counter=0
    n_of_polygons=0
    for line in textdata:
        counter+=1
        line=line[16:-4]
        polygons=line.split("),(")
        text_out_write("Polygon"+str(counter)+"\n")
        for polygon in polygons:
            n_of_polygons+=1
            text_out.write(point+"\n")
        text_out.write("\n")
    print(n_of_points)
    print("split the stuff up into polygons")


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
        text_out.write("Polygon"+str(counter)+" ")
        for point in points:
            n_of_points+=1
            text_out.write(point+" ")
        text_out.write(" ")
    text_in.close()
    text_out.close()
    print(n_of_points)
    print("split the stuff up into points")

def cleanup_points(input_path,output_path):
    print("cleanin'")
    text_in=open(input_path,"r")
    text_out=open(output_path,"w+")
    for line in text_in:
        while("(" in line):
            line=line[1:]
        while(")" in line):
            line=line[:-1]
        text_out.write(line)
    text_in.close()
    text_out.close()
    

def process_points(input_path,output_path):
    print("splittin' it up into coordinates")
    text_in=open(input_path,"r")
    text_out=open(output_path,"w+")
    textdata=text_in.readlines()
    currline=""
    prevline=""
    for line in textdata:
        coords=line.split(" ")
        for coord in coords:
            prevline=currline
            currline=coord
            text_out.write(coord+"\n")
    text_in.close()
    text_out.close()
    print("split it up fam")
    cleanup_points("werktag_tag_dirty_coords.txt","werktag_tag_clean_coords.txt")

def format(input_path,output_path):
    print("formatting")
    text_in=open(input_path,"r")
    text_out=open(output_path,"w+")
    lines=[]
    length=0
    for line in text_in:
        length+=1
        lines.append(line)
    previous=lines[0]
    current=lines[1]
    for i in range(length):
        previous=current
        current=lines[i]
        if((("46." in previous)or("47." in previous)or("45." in previous))and current!="\n"):
            text_out.write("\n")
            text_out.write(current)
        else:
            text_out.write(current)
    print("formatted")
    text_out.close()
    text_in.close()




def create_points(input_path):
    count=0
    s2points=[]
    print("creating s2points")
    text_in=open(input_path,"r")
    length=0
    for line in text_in:
        length+=1
    text_in.close()
    text_in=open(input_path,"r")
    length=length//2
    for i in range(length):
        line=text_in.readline()
        linex=line
        if ("Polygon" in str(line)):
            s2points.append(line)
            count+=1
        else:
            liney=text_in.readline()
            if((liney != "\n") and (linex!="\n")):
                text_in.readline()
                lat_lng=s2s.LatLng.from_degrees(float(linex),float(liney))
                cell=s2s.Cell.from_lat_lng(lat_lng)
                print(cell.id())
                #latlng=s2.S2LatLng.FromDegrees(float(linex),float(liney))
                #point=s2.S2Point(latlng)
                #cell=s2.S2CellId.FromDegrees(point)
                s2points.append(cell)
                count+=3
                #print(count)
                #print(linex)
            else:
                print("created points")
                text_in.close()
                return s2points
    print("created points")
    text_in.close()
    return s2points


def create_polygons(s2points):
    for i in s2points:
        print(i)
    print("creating them polygons")
    count=0
    points=[]
    polygons=[]
    for point in s2points:
        try:
            if ("Polygon" in point):
                if(points!=[]):
                    polygon=s2.S2Polygon(points)
                    polygons.append(polygon)
                points=[]
                count+=1
        except(TypeError):
            points.append(point)
    return polygons
    

def polygon_coverer(s2polygons):
    print("covering")
    coverer=s2.S2RegionCoverer()
    coverer.set_min_level(17)
    coverer.set_max_level(17)
    coverer.set_max_cells(500)
    for polygon in s2polygons:
        covering=coverer.GetCovering(region)
        print(covering)


geopackage_to_text("/home/carlo/challpr/OeVGK_layers/json_Werktag_Tag.geojson","werktag_tag.txt")
multipolygon_to_polygon("werktag_tag.txt","werktag_tag_points.txt")
# process_multipolygon("werktag_tag.txt","werktag_tag_points.txt")
# process_points("werktag_tag_points.txt","werktag_tag_dirty_coords.txt")
# format("werktag_tag_clean_coords.txt","werktag_tag_formatted_coords.txt")
# s2points=create_points("werktag_tag_formatted_coords.txt")
# s2polygons=create_polygons(s2points)
# polygon_coverer(s2polygons)