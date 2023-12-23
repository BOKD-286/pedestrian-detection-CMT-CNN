#include <boost/thread.hpp>
#include "caffe/internal_thread.hpp"

namespace caffe {

InternalThread::~InternalThread() {
  WaitForInternalThreadToExit();
}

bool InternalThread::is_started() const {
  return thread_.get() != NULL && thread_->joinable();
}


bool InternalThread::StartInternalThread() {
  if (!WaitForInternalThreadToEx