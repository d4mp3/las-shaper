# las-shaper

GUI app for .las, .xyz and .shp files.

![image](https://user-images.githubusercontent.com/61472346/227066551-4038e9c4-3fc4-4a2e-a124-59d74291fba7.png)

#
### Functions
  EXTRACT LAS CLASS - extracting specified las class\
  MERGE FILES - merging of multiple .shp or .xyz files (shapefile results are in EPSG:2178)\
  CONVERT FILE - converting las to xyz or xyz to shp\
  CLIP XYZ TO POLYGON - clipping xyz file to shapefile mask\
  GET MAX HEIGHT - assigning max height to shapefile evalueted from two .shp files (dem, dsm). Works with shapefile results from convert file function.
#
### Run virtual env and install dependencies

```
python -m venv venv
source venv/bin/activate (venv\Scripts\activate on Windows)
pip install -r requirements.txt
```
#
### Run app

```
python app.py
```
#        
### In progres:
- print log for GUI
- set crs of output shapefile

