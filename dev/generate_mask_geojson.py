# COMMAND line script to test code to create geojson masks

#%% Instances to import annotations
import sys
import os

from skimage import io
import numpy as np

sys.path.insert(0,os.path.abspath(os.path.join('..','imgseg')))
import annotationUtils

#%% Some housekeeping to setup example data
files_proc= [os.path.abspath(os.path.join('..','data','maskGenerator','img','annotation.json'))]

masks_to_create = {
  "cells": ['filled', 'edge', 'distance', 'weigthed'],
  "nuclei": ['filled', 'edge', 'distance', 'weigthed'],
}

annot_types = list(masks_to_create.keys())

annotationsImporter = annotationUtils.GeojsonImporter()

# Instance to save masks
masks = annotationUtils.MaskGenerator()

weightedEdgeMasks = annotationUtils.WeightedEdgeMaskGenerator(sigma=8, w0=10)
distMapMasks = annotationUtils.DistanceMapGenerator(truncate_distance=None)

#%% Loop over all files
for file_proc in files_proc:
    print('PROCESSING FILE:')
    print(file_proc)

    # Decompose file name
    drive, path_and_file = os.path.splitdrive(file_proc)
    path, file = os.path.split(path_and_file)
    file_base, ext = os.path.splitext(file)

    # Read annotation:  Correct class has been selected based on annot_type
    annot_dict_all, roi_size_all,image_size = annotationsImporter.load(file_proc)

    for annot_type in annot_types:

        # Filter the annotations by label
        annot_dict = {k: annot_dict_all[k] for k in annot_dict_all.keys() if annot_dict_all[k]['properties']['label'] == annot_type}

        # Create masks

        # Binary - is always necessary to creat other masks
        print(' .... creating binary masks .....')
        binaryMasks = annotationUtils.BinaryMaskGenerator(image_size = image_size, erose_size=5, obj_size_rem=500, save_indiv=True)
        mask_dict   = binaryMasks.generate(annot_dict)

        # Save binary masks FILLED if specified
        if 'filled' in masks_to_create[annot_type]:

            file_name_save = os.path.join(drive,path, annot_type + '__mask_fill.png')
            masks.save(mask_dict,'fill',file_name_save)

        # Edge mask
        if 'edge' in masks_to_create[annot_type]:
            file_name_save = os.path.join(drive,path, annot_type + '__mask_edge.png')
            masks.save(mask_dict,'edge',file_name_save)

        # Distance map
        if 'distance' in masks_to_create[annot_type]:
            print(' .... creating distance maps .....')
            mask_dict    = distMapMasks.generate(annot_dict,mask_dict)

            # Save
            file_name_save = os.path.join(drive,path, annot_type + '__mask_distMap.png')
            masks.save(mask_dict,'distance_map',file_name_save)


        # Weighted edge mask
        if 'weigthed' in masks_to_create[annot_type]:
            print(' .... creating weighted edge masks .....')
            mask_dict = weightedEdgeMasks.generate(annot_dict,mask_dict)

            # Save
            file_name_save = os.path.join(drive,path, annot_type + '__mask_edgeWeight.png')
            masks.save(mask_dict,'edge_weighted',file_name_save)
