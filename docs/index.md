
# Deep learning with ImJoy

We provide Python libraries powered by [**ImJoy**](https://imjoy.io/docs/#/) to
perform cell segmentation.

## ImJoy
[**ImJoy**](https://imjoy.io/docs/#/) is image processing platform with an easy to use interface powered by a Python engine running in the background. ImJoy plays a central role in most analysis workflows.

![ImJoyScreenshot](/img/imjoy-screenshot.png)

We provide links to install the different ImJoy plugins in dedicated ImJoy workspaces. Once installed, ImJoy remembers the workspaces and plugins and you simply have to open the web app and select the appropriate workspace [https://imjoy.io/#/app](https://imjoy.io/#/app)

If you press on the installation link, the ImJoy web app will open and display a dialog asking if you want to install the specified plugin. To confirm, press the `install` button.

![ImJoyScreenshot](/img/imjoy-installplugin.png)

Plugins require the **ImJoy Plugin Engine**, to perform computations in
Python. You will need to **install** it only once, but **launch** it each time
you work with ImJoy. For more information for how to install and use the pluging engine, please consult the [ImJoy documentation](https://imjoy.io/docs/#/user-manual?id=python-engine).

##  Segmentation with deep learning

We use deep learning to perform cell segmentation.

This requires a training step in order for the model to learn how to segment the
data. Once a model is it training it can be applied on new data.

We provide pre-trained models. While these model might already perform relatively
well on your data, re-training them might further improve their performance.

### Training
In order to train a model images have to be annotated, e.g. the biological structures
of interest highlighted in the image. These annotated images can then be used for training.

### Prediction
Once a model is trained, you can apply it on new data.
