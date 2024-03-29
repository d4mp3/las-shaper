'''
    TODO:
        - crs as functions' argument for define your own crs
'''

import geopandas as gpd
import pandas as pd
import laspy
from pathlib import Path
from numpy import savetxt
import os


def extract_las_class(inpath, outpath, las_calssification):
    print("Calling extract_las_classification")
    pathlist = [x.strip() for x in inpath.split("; ")]
    las_calssification = int(las_calssification.split(" ", 1)[0])

    # if Path(outpath).exists() is False:
    #     os.mkdir(outpath + '/las')

    # iterates through files, checks file existing, selects right lidar data class
    for counter, path in enumerate(pathlist):
        filename = Path(path).stem
        print("Processing {} ({} of {})".format(filename, counter + 1, len(pathlist)))
        if Path(outpath).exists() is False:
            input_las = laspy.read(path)
            new_file = laspy.create(
                point_format=input_las.header.point_format,
                file_version=input_las.header.version)
            new_file.points = input_las.points[input_las.classification == las_calssification]
            print("Saving results to file...")
            new_file.write(outpath)

        else:
            input_las = laspy.read(path)
            with laspy.open(outpath, mode="a") as ground_las:
                if (len(input_las.points[input_las.classification == las_calssification]) == 0):
                    continue
                else:
                    print("Saving results to file...")
                    ground_las.append_points(
                        input_las.points[input_las.classification == las_calssification])
        print("The results have been saved!")
    return None


def create_shp_from_xyz(inpath, outpath):
        print("Calling shp_from_xyz")
        df = pd.read_csv(inpath, sep='\t', header=None)
        df.columns = ['x', 'y', 'z']
        points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x'], df['y']))
        points = points.set_crs(2178, allow_override=True)
        print("Saving results to file...")
        points.to_file(outpath, mode='w')
        print("The results have been saved!")
        return None


def create_xyz_from_las(inpath, outpath):
        print("Calling create_xyz_from_las")
        las = laspy.read(inpath)
        xyz = las.xyz
        print("Saving results to file...")
        savetxt(outpath, xyz, delimiter='\t')
        print("The results have been saved!")
        return None

def merge_shp_files(inpath, outpath):
        print("Calling merge_shp_files")
        # pathlist = list(Path(inpath).glob('**/*.shp'))
        pathlist = [x.strip() for x in inpath.split("; ")]


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
        results.to_file(outpath, mode='w')

        # if Path(outpath + '/shp').exists() is False:
        #     os.mkdir(outpath + '/shp')
        #     results.to_file(outpath + '/shp/dem_results.shp', mode='w')
        # else:
        #     results.to_file(outpath + '/shp/dem_results.shp', mode='w')

        print("The results have been saved!")
        return None


def merge_xyz_files(inpath, outpath):
        print("Calling merge_xyz_files")
        pathlist = [x.strip() for x in inpath.split("; ")]
        new_file = open(outpath, 'a')

        print("Working on merge process...")
        for path in pathlist:
            xyz_file = open(path, 'r')

            for line in xyz_file.readlines():
                new_file.write(line)

        xyz_file.close()
        new_file.close()
        print("The results have been saved!")


def clip_xyz_to_poly(inpath, outpath, poly):
        print("Calling create_gdf_from_xyz")
        print("Reading shapefile")
        poly = gpd.read_file(poly)
        pathlist = [x.strip() for x in inpath.split("; ")]
        # pathlist = list(Path(inpath).glob('**/*.xyz'))

        for counter, path in enumerate(pathlist):
            filename = Path(path).stem
            print("Processing {} ({} of {})".format(filename, counter + 1, len(pathlist)))
            df = pd.read_csv(path, sep='\t', header=None)
            df.columns = ['x', 'y', 'z']
            points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x'], df['y']))
            points = points.set_crs(2178, allow_override=True)
            print("Created points GeoDataFrame")
            results = intersect_using_spatial_index(points, poly)

            if len(results) > 1:
                print("Saving results to file...")
                results.to_file(outpath, mode='w')
        print("The results have been saved!")



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


def get_max_value(poly, dem_points, dsm_points, outpath):
        print("Calling get_max_value")
        print("Loading polygon layer...")
        poly = gpd.read_file(poly)
        print("Loading dem points layer...")
        print(type(dem_points))
        dem_points = gpd.read_file(dem_points)
        print("Loading dsm points layer...")
        dsm_points = gpd.read_file(dsm_points)

        # checks if one point of points' list is in polygon geometry
        # if True joins attributes
        def spatial_join(poly, points):
            print("Calling spatial_join")
            results = poly
            for idx, x in enumerate(points):
                if poly.crs == points[idx].crs:
                    print("Processing sjoin ({} of 2)".format(idx + 1))
                    join = gpd.sjoin(points[idx], poly, how='inner', op='within')
                else:
                    print("Processing sjoin ({} of 2)".format(idx + 1))
                    points = points[idx].to_crs(poly.crs)
                    join = gpd.sjoin(points[idx], poly, how='inner', op='within')

                join['z'] = pd.to_numeric(join['z'])
                new_name = 'z_{}'.format(idx)
                join = join.rename(columns={'z': new_name})
                join = join.groupby('IDB', sort=False)[new_name].mean()

                results = results.merge(join, on='IDB', how='outer')

            return results

        outcome = spatial_join(poly, [dem_points, dsm_points])
        outcome['delta_z'] = outcome['z_1'] - outcome['z_0']

        print("Saving results to file...")
        outcome.to_file(outpath, mode='w')
        print("The results have been saved!")
