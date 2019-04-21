# Data organisation

Here we describe how the data has to be organised to perform either prediction
or training.

## Prediction

## Training

To perform training, you have to provide both the input images as well as target
images (the masks created from your annotations). These data have to be organised
according to following guidelines, resulting in an organisation as shown below.

    ├─ data_for_training/
    │  ├─ train/
    │  │  ├─ img1
    │  │  │  ├─ cells.png
    │  │  │  ├─ cells_mask_edge.png
    │  │  │  ├─ nuclei.png
    │  │  │  ├─ nuclei_mask_full.png
    │  │  ├─ img2
    │  │  │  ├─ cells.png
    │  │  │  ├─ cells_mask_edge.png
    │  │  │  ├─ nuclei.png
    │  │  │  ├─ nuclei_mask_full.png
    │  │  ...
    │  ├─ valid/
    │  │  ├─ img57
    │  │  │  ├─ cells.png
    │  │  │  ├─ cells_mask_edge.png
    │  │  │  ├─ nuclei.png
    │  │  │  ├─ nuclei_mask_full.png
    │  │  ├─ img58
    │  │  │  ├─ cells.png
    │  │  │  ├─ cells_mask_edge.png
    │  │  │  ├─ nuclei.png
    │  │  │  ├─ nuclei_mask_full.png
    │  │   ...

1.  Data has to be stored in two folders **train**, **valid**.
    The `train` folder will be used to train the neural network, the `valid` folder
    to continuously monitor how well the training worked. Both folders have to contain
    images and annotations.
2.  Each image is stored in a separate subfolder with a unique name. Across these folders,
    input and mask images have always the same name. If you use the provided ImJoy
    plugin to create masks, this will be automatically created for you.

## How many cells for training an validation?
There is no simple rule for how many images / annotated cells or nuclei you will need
to obtain good results. As an example, for standard segmentation of adherent cells, we obtained
good results with a training set of 5 images (with up to 10-15 cells per image),
and test set of 2 images. For more challenging data-sets, you can add more training
data if you see that the performance is not satisfying with the current training
data set.
