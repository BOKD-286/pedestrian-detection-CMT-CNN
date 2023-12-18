---
title: ImageNet tutorial
description: Train and test "CaffeNet" on ImageNet data.
category: example
include_in_docs: true
priority: 1
---

Brewing ImageNet
================

This guide is meant to get you ready to train your own model on your own data.
If you just want an ImageNet-trained network, then note that since training takes a lot of energy and we hate global warming, we provide the CaffeNet model trained as described below in the [model zoo](/model_zoo.html).

Data Preparation
----------------

*The guide specifies all paths and assumes all commands are executed from the root caffe directory.*

*By "ImageNet" we here mean the ILSVRC12 challenge, but you can easily train on the whole of ImageNet as well, just with more disk space, and a little longer training time.*

We assume that you already have downloaded the ImageNet training data and validation data, and they are stored on your disk like:

    /path/to/imagenet/train/n01440764/n01440764_10026.JPEG
    /path/to/imagenet/val/ILSVRC2012_val_00000001.JPEG

You will first need to prepare some auxiliary data for training. This data can be downloaded by:

    ./data/ilsvrc12/get_ilsvrc_aux.sh

The training and validation input are described in `train.txt` and `val.txt` as text listing all the files and their labels. Note that we use a different indexing for labels than the ILSVRC devkit: we sort the synset names in their ASCII order, and then label them from 0 to 999. See `synset_words.txt` for the synset/name mapping.

You may want to resize the images to 256x256 in advance. By default, we do not explicitly do this because in a cluster environment, one may benefit from resizing images in a parallel fashion, using mapreduce. For example, Yangqing used his lightweight [mincepie](https://github.com/Yangqing/mincepie) package. If you prefer things to be simpler, you can also use shell commands, something like:

    for name in /path/to/imagenet/val/*.JPEG; do
        convert -resize 256x256\! $name $name
    done

Take a look at `examples/imagenet/create_imagenet.sh`. Set the paths to the train and val dirs as needed, and set "RESIZE=true" to resize all images to 256x256 if you haven't resized the images in advance.
Now simply create the leveldbs with `examples/imagenet/create_imagenet.sh`. Note that `examples/imagenet/ilsvrc12_train_leveldb` and `examples/imagenet/ilsvrc12_val_leveldb` should not exist before this execution. It will be created by the script. `GLOG_logtostderr=1` simply dumps more information for you to inspect, and you can safely ignore it.

Compute Image Mean
------------------

The model requires us to subtract the image mean from each image, so we have to compute the mean. `tools/compute_image_mean.cpp` implements that - it is also a good example to familiarize yourself on how to manipulate the multiple components, such as protocol buffers, leveldbs, and logging, if you are not familiar with them. Anyway, the mean computation can be carried out as:

    ./examples/imagenet/make_imagenet_mean.sh

which will make `data/ilsvrc12/imagenet