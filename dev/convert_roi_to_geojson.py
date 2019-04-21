# Intended as a one time conversion of FiJi annotations to ImJoy's annotation
#  format. 

#%% Import modules
import os
import shutil
import numpy as np
from read_roi import read_roi_zip  # https://github.com/hadim/read-roi
from geojson import Polygon as geojson_polygon
from geojson import Feature, FeatureCollection, dump  # Used to create and save the geojson files: pip install geojson

# Create folders
def create_folder(folder_new):
    if not os.path.isdir(folder_new):
        os.makedirs(folder_new)


#%% Some parameters
annot_ext = '_ROI.zip'
img_ext='.tif'
path_open = '/Volumes/PILON_HD2/fmueller/Documents/Data/ImJoy/segmentation/CellMask/fijiroi'
image_size = (2048,2048)

channels =  [{'name': 'cells', 'identifier': 'Cy5'},
             {'name': 'nuclei', 'identifier': 'DAPI'} ]

# Transform channel list in dictionary with identifiers being the key
channels_new = {}
for iter, dic in enumerate(channels):
    channels_new[dic["identifier"]] = {}
    channels_new[dic["identifier"]]['name'] = dic["name"]

channel_ident = list(channels_new.keys())


#%% Recursive search to find all files
files_proc = []

for root, dirnames, filenames in os.walk(path_open):
    for filename in filenames:
        if filename.endswith(annot_ext):
            files_proc.append(os.path.join(root, filename))


#%% Loop over all files
for file_proc in files_proc:

    print(f'PROCESSING FILE: {file_proc}')

    # Decompose file name
    drive, path_and_file = os.path.splitdrive(file_proc)
    path, file = os.path.split(path_and_file)
    file_base = file.replace(annot_ext,'')

    file_ch = next((substring for substring in channel_ident if substring in file_base), None)

    if not file_ch:
        print(f'No channel identifier found in file name {file_base}')
        continue

    print(f'Mask type identified: {file_ch}')

    # Create sub-folder and remove channel identifier
    subfolder = file_base.replace(file_ch, "")
    folder_save = os.path.join(drive,path,'_anet',subfolder)
    create_folder(folder_save)


    # Open ROI file
    roi_dict_complete = read_roi_zip(file_proc)

    # Simplify dictionary & get size of annotations
    annot_dict = {}
    roi_size_all = []
    features = []   # For geojson

    for key_roi, val_roi in roi_dict_complete.items():

        # Get coordinates - maybe x and y have to be exchanged
        pos = np.column_stack((val_roi['y'], val_roi['x']))

        # Create and append feature for geojson
        pol_loop = geojson_polygon(pos.tolist())
        features.append(Feature(geometry=pol_loop,properties= {"label": channels_new[file_ch]['name']})) #,  properties={"country": "Spain"}) #)

    # Create geojson feature collection
    feature_collection = FeatureCollection(features,bbox = [0, 0.0, image_size[0], image_size[1]])

    # Save to json file
    save_name_json = os.path.join(folder_save, channels_new[file_ch]['name'] + '_annotation.json')
    with open(save_name_json, 'w') as f:
        dump(feature_collection, f)
        f.close()


    # Find and copy raw data renamed with channel identifier
    img_raw = os.path.join(drive,path,file_base+img_ext)
    if os.path.isfile(img_raw):
        img_raw_new = os.path.join(folder_save, channels_new[file_ch]['name']+img_ext)
        shutil.copy(img_raw, img_raw_new)
        print(f'Copying raw image: {img_raw}')

    else:
        print(f'Raw image does not exist: {img_raw}')
