
#!/bin/bash

set -e

mv Makefile.config.example Makefile.config

if $WITH_CUDA; then
  # Only generate compute_50.
  GENCODE="-gencode arch=compute_50,code=sm_50"
  GENCODE="$GENCODE -gencode arch=compute_50,code=compute_50"
  echo "CUDA_ARCH := $GENCODE" >> Makefile.config
fi

cat << 'EOF' >> Makefile.config
ANACONDA_HOME := $(HOME)/miniconda
PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
		$(ANACONDA_HOME)/include/python2.7 \
		$(ANACONDA_HOME)/lib/python2.7/site-packages/numpy/core/include
PYTHON_LIB := $(ANACONDA_HOME)/lib
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib
WITH_PYTHON_LAYER := 1
EOF