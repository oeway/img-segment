# Data organization

To perform training, you have to provide both the input images as well as target
images (the masks created from your annotations). These data have to be organized
according to following guidelines. Note that this strict organization is ONLY needed for training,
for prediction, data can be organized more freely.

1.  Data has to be stored in two folders **train**, **valid**.
    The `train` folder will be used to train the neural network, the `valid` folder
    to continuously monitor how well the training worked. Both folders have to contain
    images and annotations.
2.  Sub-folders then stored different field of views. Images can be stored either
    as multi-channel or mono-channel, but they must have the same name across

In an example, this could look like the organization shown below. For each

```
    ├─ data_for_training/
    │  ├─ train/
    │  │  ├─ img1
    │  │  │  ├─ cells.png
    │  │  │  ├─ nuclei.png
    │  │  ├─ img2
    │  │  │  ├─ cells.png
    │  │  │  ├─ nuclei.png
    │  │  ...
    │  ├─ valid/
    │  │  ├─ img57
    │  │  │  ├─ cells.png
    │  │  │  ├─ nuclei.png
    │  │  ├─ img58
    │  │  │  ├─ cells.png
    │  │  │  ├─ nuclei.png
    │  │   ...
```

## How many cells for training an validation?
There is no simple rule for how many images / annotated cells or nuclei you will need
to obtain good results. As an example, for standard segmentation of adherent cells, we obtained
good results with a training set of 5 images (with up to 10-15 cells per image),
and test set of 2 images. For more challenging data-sets, you can add more training
data if you see that the performance is not satisfying with the current training
data set.
