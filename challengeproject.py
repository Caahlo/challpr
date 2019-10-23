import itertools
import csv
import geopandas as gpd
import s2_py as s2
from shapely.geometry import polygon as shapely_polygon, MultiPolygon as shapely_MultiPolygon

def main():
    converter("oevgk18_2018_11_13_Tag", "werktag_tag_grades.csv")
    converter("oevgk18_2018_11_13_Abend", "werktag_abend_grades.csv")
    converter("oevgk18_2018_11_10_Tag", "samstag_tag_grades.csv")
    converter("oevgk18_2018_11_10_Nacht", "samstag_nacht_grades.csv")
    converter("oevgk18_2018_11_18_Tag", "sonntag_tag_grades.csv")
    converter("oevgk18_2018_11_18_Nacht", "sonntag_nacht_grades.csv")

def converter(layer, csv_file):
    layer_df = read_gdb("Final_OeVGK_2018.gdb.zip", layer)
    polys = convert(layer_df)
    layer_df['covering'] = polys.apply(compute_covering)
    grade_dictionary = assign_grade(layer_df)
    write_to_csv(grade_dictionary, csv_file)
    print("converted "+layer)

def read_gdb(file, layer_name):
    layer = gpd.read_file(file, layer=layer_name)
    layer = layer.to_crs({'init': 'epsg:4326'})
    layer.geometry = layer.geometry.apply(fix_geometry)
    return layer

def convert(layer_df):
    return layer_df.geometry.apply(s2anypoly)

def compute_covering(s2polygon):
    coverer = s2.S2RegionCoverer()
    coverer.set_min_level(17)
    coverer.set_max_level(17)
    coverer.set_max_cells(100)
    covering = coverer.GetCovering(s2polygon)
    return covering

def assign_grade(layer_df):
    dictionary = {}
    for _, row in layer_df.iterrows():#the underscore stands for an unused variable
        grade = row.grade
        covering = row.covering
        for cell in covering:
            cell_id=hex(cell.id())
            old_grade = dictionary.get(cell_id, "Z")
            dictionary[cell_id] = min(grade, old_grade)
    return dictionary

def write_to_csv(dictionary,output):
    with open(output, 'w') as csv_file:
        for key in dictionary.keys():
            csv_file.write("%s,%s\n"%(key,dictionary[key]))

def s2anypoly(geom):
    if type(geom) is shapely_MultiPolygon:
        return s2multipoly(geom)
    else:
        assert type(geom) is shapely_polygon.Polygon
        return s2singlepoly(geom)

def fix_geometry(geometry):
    fixed_geom = geometry.buffer(0)
    assert fixed_geom.is_valid
    return fixed_geom

def s2multipoly(multipolygon) -> s2.S2Polygon:  # a S2 "Polygon" can represent an OGC / Shapely MultiPolygon
    assert multipolygon.is_valid
    assert type(multipolygon) is shapely_MultiPolygon
    polygons = multipolygon.geoms

    rings = itertools.chain.from_iterable(extract_rings(polygon) for polygon in polygons)
    s2loops = [s2loop(ring) for ring in rings]
    result = s2.S2Polygon()
    result.InitNested(s2loops)
    return result

def s2singlepoly(polygon) -> s2.S2Polygon:  # a S2 "Polygon" can represent an OGC / Shapely Polygon
    assert polygon.is_valid
    assert type(polygon) is shapely_polygon.Polygon

    rings = extract_rings(polygon)
    s2loops = [s2loop(ring) for ring in rings]
    result = s2.S2Polygon()
    result.InitNested(s2loops)
    return result

def extract_rings(polygon_unoriented):
    polygon_oriented = shapely_polygon.orient(polygon_unoriented, 1.0)
    return [polygon_oriented.exterior, *polygon_oriented.interiors]

def s2loop(ring: shapely_polygon.LinearRing):
    s2points = [s2point(coord_pair) for coord_pair in ring.coords]
    result = s2.S2Loop(s2points)
    result.Normalize()  # orient so that at most 1/2 sphere is enclosed
    return result

def s2point(coord_pair):
    lng, lat = coord_pair
    latlng = s2.S2LatLng.FromDegrees(lat, lng)
    point = latlng.ToPoint()
    return point

if __name__ == "__main__":
    main()