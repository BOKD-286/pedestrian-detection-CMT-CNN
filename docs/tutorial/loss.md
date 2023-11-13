---
title: Loss
---
# Loss

In Caffe, as in most of machine learning, learning is driven by a **loss** function (also known as an **error**, **cost**, or **objective** function).
A loss function specifies the goal of learning by mapping parameter settings (i.e., the current network weights) to a scalar value specifying the  "badness" of these parameter settings.
Hence, the goal of learning is to find a setting of the weights that *minimizes* the loss function.

The loss in Caffe is computed by the Forward pass of the network.
Each layer takes a set of input (`bottom`) blobs and produces a set of output (`top`) blobs.
Some of these layers' outputs may be used in the loss function.
A typical choice of loss function for one-versus-all classificati