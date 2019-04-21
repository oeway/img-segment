# Code to post-process segmentation results 
#  Part about actual cell segmentation comes from https://gitlab.pasteur.fr/wouyang/im2im-segmentation:
#    ==> run_im2im.py --> calls segment_cells_nuclei (from im2imLib.segmentationUtils)
#
# Test files: on GitHub: img-segment/data/postprocessing/outputs/data/postprocessing/mask2json


#%% Test modules
import sys
import os
import importlib

from skimage import io
import numpy as np
from geojson import Feature, FeatureCollection, dump  # Used to create and save the geojson files: pip install geojson

sys.path.insert(0,os.path.abspath(os.path.join('..','imgseg')))


#%% Loop over files and perform postprocessing
import segmentationUtils
importlib.reload(segmentationUtils)

#%% Process one folder and save as one json file allowing multiple annotation types
simplify_tol = 1     # Tolerance for polygon simplification with shapely (0 to not simplify)

outputs_dir = os.path.abspath(os.path.join('..','data','postProcessing','mask2json'))
if os.path.exists(outputs_dir):
    
    print(f'Analyzing folder:{outputs_dir}')
    features = []   # For geojson
    for file in [f for f in os.listdir(outputs_dir) if '_filled_output.png' in f]:
        
        # Read png with mask
        print(f'Analyzing file:{file}')
        
        file_full = os.path.join(outputs_dir, file)
        mask_img = io.imread(file_full)
                          
        # Get label from file name
        label = file.split('_filled_output.png', 1)[0]
        
        # Call function to transform segmentation masks into (geojson) polygons       
        features,contours  = segmentationUtils.masks_to_polygon(mask_img,
                                           features = features,
                                           label = label,
                                           simplify_tol=simplify_tol,
                                           plot_simplify=False,
                                           save_name=None)
        
    # Here summarizing the geojson should occur
    image_size = mask_img.shape  # This might cause problems if any kind of binning was performed
    feature_collection = FeatureCollection(features,bbox = [0, 0.0, image_size[0], image_size[1]])

    # Save to json file
    save_name_json = os.path.join(outputs_dir,'prediction.json')
    with open(save_name_json, 'w') as f:
        dump(feature_collection, f)
        f.close() 