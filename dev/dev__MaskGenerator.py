#%% Test files
file_open_geojson = '/Volumes/PILON_HD2/fmueller/Documents/Data/ImJoy/Segmentation__smFISH/annotated_CellMaskNew/train/w1_bac_kif1c_6512_p02/w1_bac_kif1c_6512_p02_DAPI_annotation.json'
file_open_fiji    = '/Volumes/PILON_HD2/fmueller/Documents/Data/ImJoy/Segmentation__smFISH/annotated_CellMaskNew/train/w1_bac_kif1c_6512_p02/w1_bac_kif1c_6512_p02_Cy5_ROI.zip'
file_open         = file_open_geojson


#%% Test modules
import importlib  # to reload: importlib.reload(AnnotationImporter
import sys
import os
sys.path.append('/Volumes/PILON_HD2/fmueller/Documents/code/ImJoy_dev/img-segment/imgseg')

#%% Test function - process file
import annotationUtils
importlib.reload(annotationUtils)

annotationUtils.proc_files(path_open = file_open_fiji,
                          channels = [{'name': 'Cells', 'identifier': 'Cy5', 'masks': ['edge', 'distance']}, {'name': 'Nuclei', 'identifier': 'DAPI', 'masks': ['filled']}],
                          annot_type = 'fiji',
                          annot_ext =  'ROI.zip',
                          search_recursive = False,
                          image_size = (2048,2048))


#%% Test function - read annotations from FIJI 
import annotationUtils
importlib.reload(annotationUtils)

annotationsFiji = annotationUtils.FijiImporter()
file_open = file_open_fiji
annot_dict, roi_size_all = annotationsFiji.load(file_open_fiji)


#%% Test function - read annotations from  GeoJson 
import annotationUtils
importlib.reload(annotationUtils)

annotationsGeoJson= annotationUtils.GeojsonImporter()
file_open = file_open_geojson
annot_dict, roi_size_all = annotationsGeoJson.load(file_open_geojson)


#%% Test function -  Create binary masks
importlib.reload(annotationUtils)

binaryMasks = annotationUtils.BinaryMaskGenerator(image_size = (2048,2048), erose_size=5, obj_size_rem=500, save_indiv=True)
mask_dict = binaryMasks.generate(annot_dict)


#%% Test function -  Create weighted edge masks
importlib.reload(annotationUtils)

weightedEdgeMasks = annotationUtils.WeightedEdgeMaskGenerator(sigma=8, w0=10)
mask_dict = weightedEdgeMasks.generate(annot_dict,mask_dict)


#%% Test function -  Create distance map
importlib.reload(annotationUtils)

distMapMasks = annotationUtils.DistanceMapGenerator(truncate_distance=None)
mask_dict    = distMapMasks.generate(annot_dict,mask_dict)


#%% Save masks
importlib.reload(annotationUtils)
masks = annotationUtils.MaskGenerator()

# Decompose file-names
drive, path_and_file = os.path.splitdrive(file_open)
path, file = os.path.split(path_and_file)
file_base, ext = os.path.splitext(file)

# Filled mask
file_name_save = os.path.join(drive,path, file_base + '__MASK_fill.png')
masks.save(mask_dict,'fill',file_name_save)

# Edge mask
file_name_save = os.path.join(drive,path, file_base + '__MASK_edge.png')
masks.save(mask_dict,'edge',file_name_save)


# Distance map
file_name_save = os.path.join(drive,path, file_base + '__MASK_distMap.png')
masks.save(mask_dict,'distance_map',file_name_save)

# Weighted edge
file_name_save = os.path.join(drive,path, file_base + '__MASK_edgeWeight.png')
masks.save(mask_dict,'edge_weighted',file_name_save)














#%% Test parts of modules
from read_roi import read_roi_zip  # https://github.com/hadim/read-roi
import numpy as np
import json


#%% Read FIJI region
roi_dict_complete = read_roi_zip(file_open_fiji)


# Simplify dictionary & get size of annotations
annot_dict_fiji = {}
roi_size_all = []

for key_roi, val_roi in roi_dict_complete.items():

    # Simplified dictionary: coordinates and annotation type
    annot_dict_fiji[key_roi] = {}
    annot_dict_fiji[key_roi]['pos'] = np.column_stack(
        (val_roi['y'], val_roi['x']))
    annot_dict_fiji[key_roi]['type'] = val_roi['type']

    # Store size of regions
    roi_size_all.append(
        [annot_dict_fiji[key_roi]['pos'][:, 0].max() -
         annot_dict_fiji[key_roi]['pos'][:, 0].min(),
         annot_dict_fiji[key_roi]['pos'][:, 1].max()
         - annot_dict_fiji[key_roi]['pos'][:, 1].min()])

#%% Read geojson
with open(file_open_geojson, encoding='utf-8-sig') as fh:
    data_json = json.load(fh)
    
# Loop over list and create simple dictionary & get size of annotations
annot_dict_json = {}    
for feat_idx, feat in enumerate(data_json['features']):
    #print(feat['geometry']['type'])
    #print()

    key_annot = 'annot_'+str(feat_idx)
    annot_dict_json[key_annot] = {}
    annot_dict_json[key_annot]['type'] = feat['geometry']['type']
    annot_dict_json[key_annot]['pos'] = np.squeeze(np.asarray(feat['geometry']['coordinates']))




#%% Loop over all files for processing 
channels = [{'name': 'Cells', 'identifier': 'Cy5', 'masks': ['edge', 'distance']}, {'name': 'Nuclei', 'identifier': 'DAPI', 'masks': ['filled']}]
annot_type = 'fiji'
annot_ext='ROI.zip'

#
pathOpen = '/Volumes/PILON_HD2/fmueller/Documents/Data/ImJoy/Segmentation__smFISH/annotated_CellMaskNew/train/w1_bac_kif1c_6512_p02'
pattern = 'ROI.zip'
search_recursive = True
files_proc = []


if os.path.isfile(pathOpen):
    print('Will processed ONE file')
    files_proc.append(pathOpen)
    
else:
    print('DIRECTORY')
    
    if search_recursive == True:
        print('Will search directory recursively')
        # Recursive search of specified directory 
        for root, dirnames, filenames in os.walk(pathOpen):
            for filename in filenames:
                if filename.endswith(pattern):
                    files_proc.append(os.path.join(root, filename))
    
    else:   
        # Only search current directory
        print('Will search current directory')
        filenames = os.listdir(pathOpen)
        for filename in filenames:
            if filename.endswith(pattern):
                files_proc.append(os.path.join(pathOpen, filename))
    
print(files_proc)


#%% Analyze list

# Instances to import annotations
import annotationUtils
importlib.reload(annotationUtils)

if annot_type == 'fiji':
     annotationsImporter = annotationUtils.FijiImporter()
elif annot_type == 'geoson':
    annotationsImporter = annotationUtils.GeojsonImporter()

# Instance to save masks
masks = annotationUtils.MaskGenerator()
    
# Instances to to create masks
binaryMasks = annotationUtils.BinaryMaskGenerator(image_size = (2048,2048), erose_size=5, obj_size_rem=500, save_indiv=True)
weightedEdgeMasks = annotationUtils.WeightedEdgeMaskGenerator(sigma=8, w0=10)
distMapMasks = annotationUtils.DistanceMapGenerator(truncate_distance=None)    
    
# Transform channel list in dictionary    
channels_new = {}
for iter, dic in enumerate(channels):
    channels_new[dic["identifier"]] = {}
    
    channels_new[dic["identifier"]]['name'] = dic["name"]
    channels_new[dic["identifier"]]['masks'] = dic["masks"]

channel_ident = list(channels_new.keys())

# Loop over all files
for file_proc in files_proc:
    print('PROCESSING FILE:')
    print(file_proc)

    # Decompose file name    
    drive, path_and_file = os.path.splitdrive(file_proc)
    path, file = os.path.split(path_and_file)
    file_base, ext = os.path.splitext(file)

    # Check which channel this is
    #  [ToDo]: Not perfect since it returns the first hit. 
    file_ch = next((substring for substring in channel_ident if substring in file_base), None)
    
    if not file_ch:
        print(f'No channel identifier found in file name {file_base}')
        continue
    
    print(' Mask type identified: {file_ch}')
    
    # Read annotation:  Correct class has been selected based on annot_type
    annot_dict, roi_size_all = annotationsImporter.load(file_proc)

    # Create masks
    
    # Binary - is always necessary to creat other masks
    print(' .... creating binary masks .....')
    mask_dict = binaryMasks.generate(annot_dict)
    
    # Save binary masks FILLED if specified
    if 'filled' in channels_new[file_ch]['masks']:
        
        file_name_save = os.path.join(drive,path, file_base + '__MASK_fill.png')
        masks.save(mask_dict,'fill',file_name_save)

    # Edge mask
    if 'edge' in channels_new[file_ch]['masks']:
        file_name_save = os.path.join(drive,path, file_base + '__MASK_edge.png')
        masks.save(mask_dict,'edge',file_name_save)
    

    # Distance map
    if 'distance' in channels_new[file_ch]['masks']:
        print(' .... creating distance maps .....')
        mask_dict    = distMapMasks.generate(annot_dict,mask_dict)
        
        
        # Distance map
        file_name_save = os.path.join(drive,path, file_base + '__MASK_distMap.png')
        masks.save(mask_dict,'distance_map',file_name_save)

    
    # Weighted edge mask
    if 'weigthed' in channels_new[file_ch]['masks']:
        print(' .... creating weighted edge masks .....')
        mask_dict = weightedEdgeMasks.generate(annot_dict,mask_dict)
    
        # Save
        file_name_save = os.path.join(drive,path, file_base + '__MASK_edgeWeight.png')
        masks.save(mask_dict,'edge_weighted',file_name_save)


#%% Print edge mask corresponding to first iterator item
import matplotlib.pyplot as plt

data_key = next(iter(annotatFiles))
print(data_key)

fig, (ax1 ,ax2) = plt.subplots(2,1)
ax1.imshow(annotatFiles[data_key]['image'])
#ax2.imshow(annotatFiles[data_key]['mask_edge'])
ax2.imshow(annotatFiles[data_key]['distance_map'])

                  
#%% Create zip file and delete original folder
file_name_zip = os.path.join(path_open, 'unet_data')
shutil.make_archive(file_name_zip, 'zip', path_save_unet)

if os.path.isdir(path_save_unet):
    shutil.rmtree(path_save_unet)