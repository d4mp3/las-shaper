import geopandas as gpd
import pandas as pd
import laspy
from pathlib import Path
from numpy import savetxt
import time


OUT_PATH = './data/exports'
IN_LAS = './data/las'
IN_XYZ = './data/xyz'
DEM_XYZ = './data/exports/dem.xyz'
bud_file = './data/shp/buildings.shp'
buildings = gpd.read_file(bud_file)

test_points = gpd.read_file('./data/shp/points_test.shp')


def extract_las_class(in_path, out_path):
    pathlist = Path(in_path).glob('**/*.las')
    results = out_path + '/las_result.las'

    for path in pathlist:
        if Path(results).exists() is False:
            input_las = laspy.read(path)
            new_file = laspy.create(
                point_format=input_las.header.point_format, 
                file_version=input_las.header.version)
            new_file.points = input_las.points[input_las.classification == 6]
            new_file.write(results)

        else:
            print(path)
            input_las = laspy.read(path)
            with laspy.open(results, mode="a") as ground_las:
                if (len(input_las.points[input_las.classification == 6]) == 0):
                    continue
                else:
                    ground_las.append_points(
                        input_las.points[input_las.classification == 6])

    return results


def create_xyz_from_las(las, out_path):
    las = laspy.read(las)
    xyz = las.xyz
    savetxt(out_path + '/buildings_xyz.xyz', xyz, delimiter=' ')


def merge_xyz_files(in_path, out_path):
    pathlist = Path(in_path).glob('**/*.xyz')
    new_file = open(out_path + '/dem.xyz', 'a')

    for path in pathlist:
        xyz_file = open(path, 'r')

        for line in xyz_file.readlines():
            new_file.write(line)

    xyz_file.close()
    new_file.close()


def create_gdf_from_xyz(in_path, out_path, poly):
    pathlist = Path(in_path).glob('**/*.xyz')

    for path in pathlist:

        df = pd.read_csv(path, sep='\t', header = None)
        df.columns = ['x', 'y', 'z']
        points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x'], df['y']))
        
        return intersect_using_spatial_index(points, poly)
       

def intersect_using_spatial_index(source_gdf, intersecting_gdf):
    """
    Conduct spatial intersection using spatial index for candidates GeoDataFrame to make queries faster.
    Note, with this function, you can have multiple Polygons in the 'intersecting_gdf' and it will return all the points 
    intersect with ANY of those geometries.
    """
    source_sindex = source_gdf.sindex
    possible_matches_index = []
    
    # 'itertuples()' function is a faster version of 'iterrows()'
    for other in intersecting_gdf.itertuples():
        bounds = other.geometry.bounds
        c = list(source_sindex.intersection(bounds))
        possible_matches_index += c
    
    # Get unique candidates
    unique_candidate_matches = list(set(possible_matches_index))
    possible_matches = source_gdf.iloc[unique_candidate_matches]

    # Conduct the actual intersect
    result = possible_matches.loc[possible_matches.intersects(intersecting_gdf.unary_union)]
    return result

        
start_time = time.time()
b = create_gdf_from_xyz(IN_XYZ, OUT_PATH, buildings)
# b.to_file('./data/shp/results_test.shp')
print("--- %s seconds ---" % (time.time() - start_time))

# print("Calling extract_las_classification")
# trimmed_las = extract_las_class(IN_LAS, OUT_PATH)
# print("Calling create_xyz_from_las")
# create_xyz_from_las(trimmed_las, OUT_PATH)
# print("Calling merge_multiple_xyz_files")
# merge_xyz_files(IN_XYZ, OUT_PATH)
# print("Calling create_gdf_from_xyz")


# a = inside_polygon(test_points, buildings)

# a.to_file('./data/shp/results_test.shp')
