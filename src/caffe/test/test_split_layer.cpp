#include <cstring>
#include <string>
#include <vector>

#include "google/protobuf/text_format.h"
#include "gtest/gtest.h"

#include "caffe/blob.hpp"
#include "caffe/common.hpp"
#include "caffe/filler.hpp"
#include "caffe/proto/caffe.pb.h"
#include "caffe/util/insert_splits.hpp"
#include "caffe/vision_layers.hpp"

#include "caffe/test/test_caffe_main.hpp"
#include "caffe/test/test_gradient_check_util.hpp"

namespace caffe {

template <typename TypeParam>
class SplitLayerTest : public MultiDeviceTest<TypeParam> {
  typedef typename TypeParam::Dtype Dtype;

 protected:
  SplitLayerTest()
      : blob_bottom_(new Blob<Dtype>(2, 3, 6, 5)),
        blob_top_a_(new Blob<Dtype>()),
        blob_top_b_(new Blob<Dtype>()) {
    // fill the values
    FillerParameter filler_param;
    GaussianFiller<Dtype> filler(filler_param);
    filler.Fill(this->blob_bottom_);
    blob_bottom_vec_.push_back(blob_bottom_);
    blob_top_vec_.push_back(blob_top_a_);
    blob_top_vec_.push_back(blob_top_b_);
  }
  virtual ~SplitLayerTest() {
    delete blob_bottom_;
    delete blob_top_a_;
    delete blob_top_b_;
  }
  Blob<Dtype>* const blob_bottom_;
  Blob<Dtype>* const blob_top_a_;
  Blob<Dtype>* const blob_top_b_;
  vector<Blob<Dtype>*> blob_bottom_vec_;
  vector<Blob<Dtype>*> blob_top_vec_;
};

TYPED_TEST_CASE(SplitLayerTest, TestDtypesAndDevices);

TYPED_TEST(SplitLayerTest, TestSetup) {
  typedef typename TypeParam::Dtype Dtype;
  LayerParameter layer_param;
  SplitLayer<Dtype> layer(layer_param);
  layer.SetUp(this->blob_bottom_vec_, this->blob_top_vec_);
  EXPECT_EQ(this->blob_top_a_->num(), 2);
  EXPECT_EQ(this->blob_top_a_->channels(), 3);
  EXPECT_EQ(this