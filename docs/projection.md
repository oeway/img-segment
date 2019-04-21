# 2D projections

Image segmentation is performed in 2D. 3D images thus have to transformed into
2D images with a projection along Z. We provide a plugin to perform such projections,
where we provide different approaches.

The easiest method to achieve is the so-called **maximum intensity projection (MIP)**,
where for each XY position the highest pixel value along the z-axis is used.
