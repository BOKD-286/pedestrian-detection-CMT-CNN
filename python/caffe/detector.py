#!/usr/bin/env python
"""
Do windowed detection by classifying a number of images/crops at once,
optionally using the selective search window proposal method.

This implementation follows ideas in
    Ross Girshick, Jeff Donahue, Trevor Darrell, Jitendra Malik.
    Rich feature hierarchies for accurate object detection and semantic
    segmentation.
    http://arxiv.org/abs/1311.2524

The selective_search_ijcv_with_python code required for the selective search
proposal mode is available at
    https://github.com/sergeyk/selective_search_ijcv_with_python
"""
import numpy as np
import os

import caffe


class Detector(caffe.Net):
    """
    Detector extends Net for windowed detection by a list of crops or
    selective search proposals.

    Parameters
    ----------
    mean, input_scale, raw_scale, channel_swap : params for preprocessing
        options.
    context_pad : amount of surrounding context to take s.t. a `context_pad`
        sized border of pixels in the network input image is context, as in
        R-CNN feature extraction.
    """
    def __init__(self, model_file, pretrained_file, mean=None,
                 input_scale=None, raw_scale=None, channel_swap=None,
                 context_pad=None):
        caffe.Net.__init__(self, model_file, pretrained_file, caffe.TEST)

        # configure pre-processing
        in_ = self.inputs[0]
        self.transformer = caffe.io.Transformer(
            {in_: self.blobs[in_].data.shape})
        self.transformer.set_transpose(in_, (2, 0, 1))
        if mean is not None:
            self.transformer.set_mean(in_, mean)
        if input_scale is not None:
            self.transformer.set_input_scale(in_, input_scale)
        if raw_scale is not None:
            self.transformer.set_raw_scale(in_, raw_scale)
        if channel_swap is not None:
            self.transformer.set_channel_swap(in_, channel_swap)

        self.configure_crop(context_pad)

    def detect_windows(self, images_windows):
        """
        Do windowed detection over given images and windows. Windows are
        extracted then warped to the input dimensions of the net.

        Parameters
        ----------
        images_windows: (image filename, window list) iterable.
        context_crop: size of context border to crop in pixels.

        Returns
        -------
        detections: list of {filename: image filename, window: crop coordinates,
            predictions: prediction vector} dicts.
        """
        # Extract windows.
        window_inputs = []
        for image_fname, windows in images_windows:
            image = caffe.io.load_image(image_fname).astype(np.float32)
            for window in windows:
                window_inputs.append(self.crop(image, window))

        # Run through the net (warping windows to input dimensions).
        in_ = self.inputs[0]
        caffe_in = np.zeros((len(window_inputs), window_inputs[0].shape[2])
                            + self.blobs[in_].data.shape[2:],
                            dtype=np.float32)
        for ix, window_in in enumerate(window_inputs):
            caffe_in[ix] = self.transformer.preprocess(in_, window_in)
        out = self.forward_all(**{in_: caffe_in})
        predictions = out[self.outputs[0]].squeeze(axis=(2, 3))

        # Package predictions with images and windows.
        detections = []
        ix = 0
        for image_fname, windows in images_windows:
            for window in windows:
                detections.append({
                    'window': window,
                    'prediction': predictions[ix],
                    'filename': image_fname
                })
                ix += 1
        return detections

    def detect_selective_search(self, image_fnames):
        """
        Do windowed detection over Selective Search proposals by extracting
        the crop and warping to the input dimensions of the net.

        Parameters
        ----------
        image_fnames: list

        Returns
        -------
        detections: list of {filename: image filename, window: crop coordinates,
            predictions: prediction vector} dicts.
        """
        import selective_search_ijcv_with_python as selective_search
        # Make absolute paths so MATLAB can find the files.
        image_fnames = [os.path.abspath(f) for f in image_fnames]
        windows_list = selective_search.get_windows(
            image_fnames,
            cmd='selective_search_rcnn'
        )
        # Run windowed detection on the selective search list.
        return self.detect_windows(zip(image_fnames, windows_list))

    def crop(self, im, window):
        """
        Crop a window from the image for detection. Include surrounding context
        according to the `context_pad` configuration.

        Parameters
        ----------
        im: H x W x K image ndarray to crop.
        window: bounding box coordinates as ymin, xmin, ymax, xmax.

        Returns
        -------
        crop: cropped window.
        """
        # Crop window from the image.
        crop = im[window[0]:window[2], window[1]:window[3]]

        if self.context_pad:
            box = window.copy()
            crop_size = self.blobs[self.inputs[0]].width  # assumes square
            scale = crop_size / (1. * crop_size - self.context_pad * 2)
            # Crop a box + surrounding context.
            half_h = (box[2] - box[0] + 1) / 2.
            half_w = (box[3] - box[1] + 1) / 2.
            center = (box[0] + half_h, box[1] + half_w)
            scaled_dims = scale * np.array((-half_h, -half_w, half_h, half_w))
            box = np.round(np.tile(center, 2) + scaled_dims)
            full_h = box[2] - box[0] + 1
            full_w = box[3] - box[1] + 1
            scale_h = crop_size / full_h
            scale_w = crop_size / full_w
            pad_y = round(max(0, -box[0]) * scale_h)  # amount out-of-bounds
            pad_x = rou