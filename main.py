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


def create_gdf_from_multiple_xyz(xyz_file):
    new_data = gpd.GeoDataFrame()
    new_data['geometry'] = None
    xyz_file = open(xyz_file, 'r')
    count = 0
    dataframes = []

    while True:
        line = xyz_file.readline()
        if not line:
            print("END OF FILE")
            break

        line = line.split()
        df = pd.DataFrame({'x': [float(line[0])], 'y': [
                          float(line[1])], 'z': [float(line[2])]})
        # geometry = gpd.points_from_xy(df['x'], df['y'], df['z'])
        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df['x'], df['y']))
        inside_polygon(gdf, buildings, df, dataframes)

        print("Processed {} lines".format(count+1))
        count += 1

    return gpd.GeoDataFrame(pd.concat(dataframes, ignore_index=True, 
                                      crs=dataframes[0].crs))


def create_gdf_from_single_xyz(in_path, out_path):
    pathlist = Path(in_path).glob('**/*.xyz')

    for path in pathlist:
        dataframes = []
        xyz_file = open(path, 'r')
        count = 0
        results = []
        
        # print(results.crs)
        for line in xyz_file.readlines():
            line = line.split()
            df = pd.DataFrame({'x': [float(line[0])], 'y': [float(line[1])],
                               'z': [float(line[2])]})
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x'],
                                                                   df['y']))
        
            a = inside_polygon(gdf['geometry'], buildings)
            
            if a is True:
                dataframes.append(gdf)
            
            
            if count > 1000:
                break
            
            
            print("Processed {} lines".format(count+1))
            count += 1

        return gpd.GeoDataFrame(pd.concat(dataframes, ignore_index=True))
        break

def inside_polygon(geom, poly):
    for row in poly.iterrows():
        if str(geom.within(row[1][13])[0]) == 'True':
            return True
        
        
start_time = time.time()
b = create_gdf_from_single_xyz(IN_XYZ, OUT_PATH)
b.to_file('./data/shp/results_test.shp')
print("--- %s seconds ---" % (time.time() - start_time))

# print("Calling extract_las_classification")
# trimmed_las = extract_las_class(IN_LAS, OUT_PATH)
# print("Calling create_xyz_from_las")
# create_xyz_from_las(trimmed_las, OUT_PATH)
# print("Calling merge_multiple_xyz_files")
# merge_xyz_files(IN_XYZ, OUT_PATH)
print("Calling create_gdf_from_xyz")


# a = inside_polygon(test_points, buildings)

# a.to_file('./data/shp/results_test.shp')
