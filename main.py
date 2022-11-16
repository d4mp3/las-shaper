'''
    TODO:    

        - crs as functions' argument for define your own crs
        - accessing of more attributes for spatial_join function
        - create App class
        - create common load_files_path function
        - create common save_files function
        - try to ommit converting las file to xyz for dem_handler purposes
        
'''
import geopandas as gpd
import pandas as pd
import laspy
from pathlib import Path
from numpy import savetxt
import os

OUTPATH = './data/exports'
IN_LAS = './data/las'
IN_XYZ = './data/xyz'
DEM_XYZ = './data/exports/dem.xyz'
bud_file = './data/shp/buildings.shp'
buildings = gpd.read_file(bud_file)

def extract_las_class(inpath, outpath):
    print("Calling extract_las_classification")
    pathlist = list(Path(inpath).glob('**/*.las'))
    out = outpath + '/las' + '/las_result.las'
    
    if Path(outpath + '/las').exists() is False:
        os.mkdir(outpath + '/las')
    
    # iterates through files, checks file existing, selects right lidar data class
    for counter, path in enumerate(pathlist):
        filename = Path(path).stem
        print("Processing {} ({} of {})".format(filename, counter + 1, len(pathlist)))
        if Path(out).exists() is False:
            input_las = laspy.read(path)
            new_file = laspy.create(
                point_format=input_las.header.point_format, 
                file_version=input_las.header.version)
            new_file.points = input_las.points[input_las.classification == 6]
            print("Saving results to file...")
            new_file.write(out)
        else:
            input_las = laspy.read(path)
            with laspy.open(out, mode="a") as ground_las:
                if (len(input_las.points[input_las.classification == 6]) == 0):
                    continue
                else:
                    print("Saving results to file...")
                    ground_las.append_points(
                        input_las.points[input_las.classification == 6])
                    
    return outpath


def create_shp_from_xyz(xyz, outpath):
    print("Calling shp_from_xyz")
    df = pd.read_csv(xyz, sep='\t', header = None)
    df.columns = ['x', 'y', 'z']
    points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x'], df['y']))
    points = points.set_crs(2178, allow_override=True)
    
    if Path(outpath + '/shp').exists() is False:
        os.mkdir(outpath + '/shp')
        print("Saving results to file...")
        points.to_file(outpath + '/shp//buildings.shp', mode='w')
    else:
        print("Saving results to file...")
        points.to_file(outpath + '/shp//buildings_class.shp', mode='w')
        
    return points


def create_xyz_from_las(las, outpath):
    print("Calling create_xyz_from_las")
    las = laspy.read(las)
    xyz = las.xyz
    out = outpath + '/xyz' + '/buildings_xyz.xyz'
    if Path(outpath + '/xyz').exists() is False:
        os.mkdir(outpath + '/xyz')
        print("Saving results to file...")
        savetxt(out, xyz, delimiter='\t')
    else:
        print("Saving results to file...")
        savetxt(out, xyz, delimiter='\t')


def merge_shp_files(inpath, outpath):
    print("Calling merge_shp_files")
    pathlist = list(Path(inpath).glob('**/*.shp'))
   
    for counter, path in enumerate(pathlist):
        if counter == 0:
            filename = Path(path).stem
            print("Processing {} ({} of {})".format(filename, counter + 1, len(pathlist)))
            gdfs = gpd.read_file(path)
            gdfs.set_crs(2178, allow_override=True)
        else:
            filename = Path(path).stem
            print("Processing {} ({} of {})".format(filename, counter + 1, len(pathlist)))
            gdf = gpd.read_file(path)
            gdf.set_crs(2178, allow_override=True)
            gdfs = gpd.pd.concat([gdfs, gdf])
        
    results = gpd.pd.concat([gdfs])
    print("Saving results to file...")
    if Path(outpath + '/shp').exists() is False:
        os.mkdir(outpath + '/shp')
        results.to_file(outpath + '/shp/dem_results.shp', mode='w')
    else:
        results.to_file(outpath + '/shp/dem_results.shp', mode='w')


def merge_xyz_files(inpath, outpath):
    print("Calling merge_xyz_files")
    pathlist = Path(inpath).glob('**/*.xyz')
    new_file = open(outpath + '/xyz/dem.xyz', 'a')

    for path in pathlist:
        xyz_file = open(path, 'r')

        for line in xyz_file.readlines():
            new_file.write(line)

    xyz_file.close()
    new_file.close()

# cuts xyz records to the bounds of buildings
def dem_handler(inpath, outpath, poly):
    print("Calling create_gdf_from_xyz")
    pathlist = list(Path(inpath).glob('**/*.xyz'))
    
    for counter, path in enumerate(pathlist):
        filename = Path(path).stem
        print("Processing {} ({} of {})".format(filename, counter + 1, len(pathlist)))
        df = pd.read_csv(path, sep='\t', header = None)
        df.columns = ['x', 'y', 'z']
        points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x'], df['y']))
        points = points.set_crs(2178, allow_override=True)
        print("Created points GeoDataFrame")
        results = intersect_using_spatial_index(points, poly)
        
        if len(results) > 1:
            print("Saving results to file...")
            if Path(outpath + '/shp').exists() is False:
                os.mkdir(outpath + '/shp')
                results.to_file(outpath + '/shp//dem//' + filename + '.shp', mode='w')
            else:
                results.to_file(outpath + '/shp//dem//' + filename + '.shp', mode='w')
        

def intersect_using_spatial_index(source_gdf, intersecting_gdf):
    """
    Conduct spatial intersection using spatial index for candidates GeoDataFrame to make queries faster.
    Note, with this function, you can have multiple Polygons in the 'intersecting_gdf' and it will return all the points 
    intersect with ANY of those geometries.
    """
    print("Calling intersect_using_spatial_index")
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


def get_max_value(poly, dem_points, bldg_points, outpath):
    print("Calling get_max_value")
    print("Loading polygon layer...")
    poly = gpd.read_file(poly)
    print("Loading dem points layer...")
    dem_points = gpd.read_file(dem_points)
    print("Loading buildings points layer...")
    bldg_points = gpd.read_file(bldg_points)
    
    # checks if one point of points' list is in polygon geometry
    # if True joins attributes    
    def spatial_join(poly, points):
        print("Calling spatial_join")
        results = poly
        for idx, x in enumerate(points):
            if poly.crs == points[idx].crs:
                print("Processing sjoin ({} of 2)".format(idx+1))
                join = gpd.sjoin(points[idx], poly, how='inner', op='within')
            else:
                print("Processing sjoin ({} of 2)".format(idx+1))
                points = points[idx].to_crs(poly.crs)
                join = gpd.sjoin(points[idx], poly, how='inner', op='within')
            
            join['z'] = pd.to_numeric(join['z'])
            new_name = 'z_{}'.format(idx)
            join = join.rename(columns={'z': new_name})
            join = join.groupby('IDB', sort=False)[new_name].mean()
        
            results = results.merge(join, on='IDB', how='outer')
        
        return results
   
    outcome = spatial_join(poly, [dem_points, bldg_points])
    outcome['delta_z'] = outcome['z_1'] - outcome['z_0']
    
    print("Saving results to file...")
    if Path(outpath + '/shp').exists() is False:
        os.mkdir(outpath + '/shp')
        outcome.to_file(outpath + '/shp/buildings_with_max_z_value.shp', mode='w')
    else:
        outcome.to_file(outpath + '/shp/buildings_with_max_z_value.shp', mode='w')

        
# trimmed_las = extract_las_class(IN_LAS, OUTPATH)
# create_xyz_from_las(trimmed, OUTPATH)
# merge_xyz_files(IN_XYZ, OUTPATH)
# dem_handler(IN_XYZ, OUTPATH, buildings)
# create_shp_from_xyz('./data/exports/xyz/buildings_xyz.xyz', OUTPATH)
# merge_shp_files('./data/exports/shp/dem', OUTPATH)
# b = get_max_value(bud_file, './data/exports/shp/dem_results.shp', './data/exports/shp/buildings.shp', OUTPATH)
