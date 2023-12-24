// ------------------------------------------------------------------
// Fast R-CNN
// Copyright (c) 2015 Microsoft
// Licensed under The MIT License [see fast-rcnn/LICENSE for details]
// Written by Ross Girshick
// ------------------------------------------------------------------

#include <cfloat>

#include <string>
#include <utility>
#include <vector>

#include "caffe/blob.hpp"
#include "caffe/common.hpp"
#include "caffe/layer.hpp"
#include "caffe/vision_layers.hpp"
#include "caffe/proto/caffe.pb.h"

using std::max;
using std::min;
using std::floor;
using std::ceil;

#if _MSC_VER < 1800
inline double round(double x) {
	return (x > 0.0) ? floor(x + 0.5) : ceil(x - 0.5);
}
#endif

namespace caffe {

	template <typename Dtype>
	void ROIPoolingLayer<Dtype>::LayerSetUp(const vector<Blob<Dtype>*>& bottom,
		const vector<Blob<Dtype>*>& top) {
			ROIPoolingParameter roi_pool_param = this->layer_param_.roi_pooling_param();
			CHECK_GT(roi_pool_param.pooled_h(), 0)
				<< "pooled_h must be > 0";
			CHECK_GT(roi_pool_param.pooled_w(), 0)
				<< "pooled_w must be > 0";
			pooled_height_ = roi_pool_param.pooled_h();
			pooled_width_ = roi_pool_param.pooled_w();
			spatial_scale_ = roi_pool_param.spatial_scale();
			LOG(INFO) << "Spatial scale: " << spatial_scale_;
	}

	template <typename Dtype>
	void ROIPoolingLayer<Dtype>::Reshape(const vector<Blob<Dtype>*>& bottom,
		const vector<Blob<Dtype>*>& top) {
			channels_ = bottom[0]->channels();
			height_ = bottom[0]->height();
			width_ = bottom[0]->width();
			top[0]->Reshape(bottom[1]->num(), channels_, pooled_height_,
				pooled_width_);
			m