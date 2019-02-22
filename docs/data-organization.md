# Data organisation
Data has to be split into two folders **train**, **valid**, and **test**.
The `train` folder will be used to train the neural network, the `valid` folder
to continuously monitor how well the training worked. Both folders have to contain
images and annotations. The `test` folder can then be used to test the trained
network. It only needs to contain images that should be segmented.

The example below show the folder structure with a few annotated images.

```
.
├─ test/
│  ├─ C1-img30.tif
│  ├─ C1-img31.tif
│  ...
├─ train/
│  ├─ C1-img4.tif
│  ├─ C1-img4__RoiSet.zip
│  ├─ C1-img5.tif
│  ├─ C1-img5__RoiSet.zip
│  ...
├─ valid/
│  ├─ C1-img1.tif
│  ├─ C1-img1__RoiSet.zip
│  ├─ C1-img2.tif
│  ├─ C1-img2__RoiSet.zip
.
```

There is no simple rule for how many images / annotated cells or nuclei you will need
to obtain good results. As an example, for standard segmentation of adherent cells, we obtained
good results with a training set of 5 images (with up to 10-15 cells per image),
and test set of 2 images. For more challenging data-sets, you can add more training
data if you see that the performance is not satisfying with the current training
data set.
