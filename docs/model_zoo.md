---
title: Model Zoo
---
# Caffe Model Zoo

Lots of researchers and engineers have made Caffe models for different tasks with all kinds of architectures and data.
These models are learned and applied for problems ranging from simple regression, to large-scale visual classification, to Siamese networks for image similarity, to speech and robotics applications.

To help share these models, we introduce the model zoo framework:

- A standard format for packaging Caffe model info.
- Tools to upload/download model info to/from Github Gists, and to download trained `.caffemodel` binaries.
- A central wiki page for sharing model info Gists.

## Where to get trained models

First of all, we bundle BVLC-trained models for unrestricted, out of the box use.
<br>
See the [BVLC model license](#bvlc-model-license) for details.
Each one of these can be downloaded by running `scripts/download_model_binary.py <dirname>` where `<dirname>` is specified below:

- **BVLC Reference CaffeNet** in `models/bvlc_reference_caffenet`: AlexNet trained on ILSVRC 2012, with a minor variation from the version as described in [ImageNet classification with deep convolutional neural networks](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) by Krizhevsky et al. in NIPS 2012. (Trained by Jeff Donahue @jeffdonahue)
- **BVLC AlexNet** in `models/bvlc_alexnet`: AlexNet trained on ILSVRC 2012, almost exactly as described in [ImageNet classification with deep convolutional neural networks](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) by Krizhevsky et al. in NIPS 2012. (Trained by Evan Shelhamer @shelhamer)
- **BVLC Reference R-CNN ILSVRC-2013** in `models/bvlc_reference_rcnn_ilsvrc13`: pure Caffe implementation of [R-CNN](https://github.com/rbgirshick/rcnn) as described by Girshick et al. in CVPR 2014. (Trained by Ross Girshick @rbgirshick)
- **BVLC GoogLeNet** in `models/bvlc_googlenet`: GoogLeNet trained on ILSVRC 2012, almost exactly as described in [Going Deeper with Convolutions](http://arxiv.org/abs/1409.4842) by Szegedy et al. in ILSVRC 2014. (Trained by Sergio Guadarrama @sguada)

**Community models** made by Caffe users are posted to a publicly editable [wiki page](https://github.com/BVLC/caffe/wiki/Model-Zoo).
These models are subject to conditions of their respective authors such as citation and license.
Thank you for sharing your models!

## Model info format

A caffe model is distributed as a directory containing:

- Solver/model prototxt(s)
- `readme.md` containing
    - YAML frontmatter
        - Caffe version used to train this model (tagged release or commit hash).
        - [optional] file URL and SHA1 of the trained `.caffemodel`.
        - [optional] github gist id.
    - Information 