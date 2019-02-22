
# IMPORTS
import scipy
from scipy.ndimage.morphology import binary_fill_holes
from skimage.measure import label
from skimage.segmentation import find_boundaries
from skimage.filters import threshold_otsu
from scipy import ndimage
from scipy import signal
import skimage
from skimage import morphology
from skimage import filters
from skimage.morphology import disk
from skimage.morphology import greyreconstruct
from skimage import dtype_limits
import numpy as np


def _add_constant_clip(img, const_value):
    """Add constant to the image while handling overflow issues gracefully.
    """
    min_dtype, max_dtype = dtype_limits(img, clip_negative=False)

    if const_value > (max_dtype - min_dtype):
        raise ValueError("The added constant is not compatible"
                         "with the image data type.")

    result = img + const_value
    result[img > max_dtype-const_value] = max_dtype
    return(result)


def _subtract_constant_clip(img, const_value):
    """Subtract constant from image while handling underflow issues.
    """
    min_dtype, max_dtype = dtype_limits(img, clip_negative=False)

    if const_value > (max_dtype-min_dtype):
        raise ValueError("The subtracted constant is not compatible"
                         "with the image data type.")

    result = img - const_value
    result[img < (const_value + min_dtype)] = min_dtype
    return(result)

def extended_minima(img, h, selem=None):

    if np.issubdtype(img.dtype, 'half'):
        resolution = 2 * np.finfo(img.dtype).resolution
        if h < resolution:
            h = resolution
        h_corrected = h - resolution / 2.0
        shifted_img = img + h
    else:
        shifted_img = _add_constant_clip(img, h)
        h_corrected = h

    rec_img = greyreconstruct.reconstruction(shifted_img, img,
                                             method='erosion', selem=selem)
    residue_img = rec_img - img
    h_min = np.zeros(img.shape, dtype=np.uint8)
    h_min[residue_img > 0] = 1
    return h_min


def segment_cells_nuclei(image_input, image_output, h_threshold=15, min_size_cell=200, min_size_nuclei=1000, save_path=None):
    ''' Segment cells and nuclei. 
    ARGS
    image_output ... multichannel image. 1st channel is mask of the cells, 
       2nd channel mask of the nuclei.
    
    image_input  ... image of the cells used for segmentation.
    '''
    
    im_mask_cell = image_output[:, :, 0]
    im_mask_nuc  = image_output[:, :, 1]

    img_cell = image_input[:, :, 0]

    # Segment the nuclei
    nuclei_mask = segment_nuclei_cellcog(im_mask_nuc, h_threshold, min_size=min_size_nuclei)
    
    # Segment the cells
    im_binary_output = im_mask_cell > threshold_otsu(im_mask_cell)
    im_binary_output = binary_fill_holes(im_binary_output)
    im_binary_output = morphology.remove_small_objects(
        im_binary_output, min_size=min_size_cell, connectivity=1, in_place=False)
    
    # Apply watershed
    seg = morphology.watershed(
        1.0 - img_cell / 255.0, nuclei_mask, mask=im_binary_output)
    cytoplasm_mask = seg
    
    if save_path:

        import palettable
        from skimage.color import label2rgb
        
        scipy.misc.imsave(save_path + '_cell_mask.png',
                          np.float32(cytoplasm_mask))
        
        seg = label(cytoplasm_mask)
        bound = find_boundaries(seg, background=0)

        image_label_overlay = label2rgb(seg, bg_label=0, bg_color=(
            0.8, 0.8, 0.8), colors=palettable.colorbrewer.sequential.YlGn_9.mpl_colors)
        image_label_overlay[bound == 1, :] = 0

        scipy.misc.imsave(save_path + '_cell_color_mask.png',
                          np.float32(image_label_overlay))

        # tiff.imsave(img_name,np.float32(_nuclei_mask))
        scipy.misc.imsave(save_path + '_nuclei_mask.png',
                          np.float32(nuclei_mask))


        seg = label(nuclei_mask)
        bound = find_boundaries(seg, background=0)
        image_label_overlay = label2rgb(seg, bg_label=0, bg_color=(
            0.8, 0.8, 0.8), colors=palettable.colorbrewer.sequential.YlGn_9.mpl_colors)
        image_label_overlay[bound == 1, :] = 0
        scipy.misc.imsave(save_path + '_nuclei_color_mask.png',
                          np.float32(image_label_overlay))

    return cytoplasm_mask, nuclei_mask


def segment_nuclei_cellcog(im, h_threshold=10, bg_window_size=100, min_size=1000):
    im = im.astype('double')
    im = (im - im.min()) / im.max() * 255
    im = im.astype('uint8')

    # Pre-processing
    
    # Median filtering
    im_filt = filters.median(im, selem=disk(10))
    
    # BGD estimation
    window = np.ones((bg_window_size, bg_window_size)) / \
        (bg_window_size * bg_window_size)
    a = signal.fftconvolve(im_filt, window)
    crop_d = (bg_window_size - 1) // 2
    bgd_crop = a[crop_d:np.shape(im)[0] + crop_d,
                 crop_d:np.shape(im)[1] + crop_d]
    
    # BGD substraction and clip
    im_prefilt = im_filt - bgd_crop
    im_prefilt = im_prefilt.clip(min=0)
    
    # Thresholding, fill and remove small objects
    threshold = filters.threshold_otsu(im)
    img_threshold = im > threshold

    img_threshold = morphology.remove_small_objects(img_threshold, min_size)
    img_threshold = ndimage.morphology.binary_fill_holes(img_threshold)

    # Distance transform
    distance = ndimage.distance_transform_edt(img_threshold)
    distance = filters.gaussian(distance, sigma=1)

    # h-maxima detection
    res = extended_minima(-distance, h_threshold)
    label_nuc = skimage.measure.label(res)

    # watershed
    wat = morphology.watershed(-distance, label_nuc)
    result_label_seg = morphology.remove_small_objects(
        wat * img_threshold, 1000)
    return result_label_seg
