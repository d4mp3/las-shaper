# las-shaper

GUI app for .las, .xyz and .shp files.

### Functions
  EXTRACT LAS CLASS - extracting specified las class\
  MERGE FILES - merging of multiple .shp or .xyz files (shapefile results are in EPSG:2178)\
  CREATE FILES - converting las to xyz or xyz to shp\
  CLIP XYZ TO POLYGON - clipping xyz file to shapefile mask\
  ASSIGN MAX HEIGHT TO FEATURES IN SHAPEFILE - assigning max height to shapefile evalueted from two .xyz files (dem, dsm)

### Run virtual env and install dependencies

```
python -m venv venv
source venv/bin/activate (venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

### Run app

```
python app.py
```
        
### In progres:
- print log for GUI
- set crs of output shapefile

