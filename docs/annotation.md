# Image annotation

Annotations are necessary to provide a ground truth for the neural network during
training. In this step, the structures of interest, e.g. cell and nuclei, are outline in
the images to generate data that will be used to train the neural network.

We provide a dedicated plugin to perform this annotation task: the ImageAnnotor.
It was developed to integrate seamlessly in the segmentation workflow, and annotation
results are stored in the [GeoJson](http://geojson.org/) file format. Once the data
are annotated, different image masks can be generated. These mask are then used
together with the raw input images to train the network.

## Annotations in ImJoy
ImJoy provides a dedicated plugin to perform annotations.

* How to get data inside
* Different annotation types
* How to store annotations
* Explain that in one image, you can have different annotation types.
* Note that both training and test data have to be annotated
* Stored as one file `annotation.json` per folder.

As an example, for one of the images this could then look like this:

```
    ├─ data_for_training/
    │  ├─ train/
    │  │  ├─ img1
    │  │  │  ├─ annotation.json
    │  │  │  ├─ cells.tif
    │  │  │  ├─ nuclei.tif
    │  │  ├─ img2
    │  │  │  ├─ annotation.json
    │  │  │  ├─ cells.png
    │  │  │  ├─ nuclei.png
    │  │  ...
```

## Convert annotations to mask images

Once you have annotated the images, you have to convert these annotations to
mask images, which are used as input for the neural network. We provide a dedicated ImJoy
plugin to perform this task.

* Screen shot

I allows to specify for each of the annotation types different mask images. We support
the following four masks

* Show examples

You can then select either one annotation file, or recursively search a folder
for all `annotation.json` files

As an example, for one of the images this could then look like this:

```
    ├─ data_for_training/
    │  ├─ train/
    │  │  ├─ img1
    │  │  │  ├─ annotation.json
    │  │  │  ├─ cells.tif
    │  │  │  ├─ cells_mask_edge.png
    │  │  │  ├─ nuclei.tif
    │  │  │  ├─ nuclei_mask_full.png

```
