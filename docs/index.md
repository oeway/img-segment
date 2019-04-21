
# Deep learning with ImJoy

We provide a complete framework to perform image segmentation with Deep learning
powered by [**ImJoy**](https://imjoy.io/docs/#/). We provide an integrated solution
ranging from the creation of training data, over perform the actual training, and
applying the trained models on new data.


## ImJoy
[**ImJoy**](https://imjoy.io/docs/#/) is image processing platform with an easy to use interface powered by a Python engine running in the background. ImJoy plays a central role in most analysis workflows.

![ImJoyScreenshot](/img/imjoy-screenshot.png)

We provide links to install the different ImJoy plugins. If you press on the installation link,
the ImJoy browser app will open and display a dialog asking if you want to
install the specified plugin. To confirm, press the `install` button.

![ImJoyScreenshot](/img/imjoy-installplugin.png)

The plugins will be installed in the dedicated workspace `segmentation`. ImJoy
will store this workspace and the plugins in your browser, and the use it another
time you have to simply open the browser app and select the appropriate
workspace [https://imjoy.io/#/app](https://imjoy.io/#/app)

Some of the plugins, e.g. for to train a neural network, require the **ImJoy Plugin Engine**.
You will need to **install** it only once, but **launch** it each time
you work with ImJoy. For more information for how to install and use the plugin engine, please consult the [ImJoy documentation](https://imjoy.io/docs/#/user-manual?id=python-engine).

##  Segmentation with deep learning
We use the popular [U-net framework](https://www.nature.com/articles/s41592-018-0261-2)
to perform the segmentation task. As other deep learning methods, this requires a
training step in order for the model to learn how to segment the
data. Once a model is it training it can be applied on new data.

We provide pre-trained models. While these model might already perform relatively
well on your data, re-training them might further improve their performance.

### Training
In order to train a model images have to be annotated, e.g. the biological structures
of interest highlighted in the image. These annotated images can then be used for training.

### Prediction
Once a model is trained, you can apply it on new data.
