# Code to post-process segmentation results 
#  Part about actual cell segmentation comes from https://gitlab.pasteur.fr/wouyang/im2im-segmentation:
#    ==> run_im2im.py --> calls segment_cells_nuclei (from im2imLib.segmentationUtils)

#%% Test modules
import sys
import os
from skimage import io
import numpy as np

sys.path.insert(0,os.path.abspath(os.path.join('..','imgseg')))


#%% Loop over files and perform postprocessing
# Test files: on GitHub: img-segment/data/postprocessing/outputs/data/postprocessing/cells_nuclei
import segmentationUtils

outputs_dir = os.path.abspath(os.path.join('..','data','postProcessing','cells_nuclei'))

h_threshold     = 15   # 15; morphological depth for nuclei separation (watershed)
min_size_cell   = 20   # 200; minimum size of cell
min_size_nuclei = 100  # 1000; minimum size of the nuclei
                       # skimage.morphology.remove_small_objects

if os.path.exists(outputs_dir):
    for file in [f for f in os.listdir(outputs_dir) if 'outputs.png' in f]:
        
        print(f'Processing file: {file}')
        
        file = os.path.join(outputs_dir, file)
        
        # Read png with input and output
        output_png = io.imread(file)
        input_png = io.imread(file.replace('outputs.png', 'inputs.png'))
            
        # Create empty arrays to store the relevant channels for postprocessing
        img_output = np.zeros((output_png.shape[0],output_png.shape[1],2))
        img_input  = np.zeros((output_png.shape[0],output_png.shape[1],1))
        
        img_output[:, :, 0] = output_png[:, :, 0]   # Cell mask
        img_output[:, :, 1] = output_png[:, :, 2]   # Nuclei mask
        
        img_output[:, :, 0] = input_png[:, :, 0]    # Image of cell
        
        
        # Call function to perform segmentation
        cytoplasm_mask, nuclei_mask = segmentationUtils.segment_cells_nuclei(img_output, 
                                       img_output,
                                       h_threshold=h_threshold, 
                                       min_size_cell=min_size_cell, 
                                       min_size_nuclei=min_size_nuclei, 
                                       save_path=file.replace('.png', '_'))
