# Copyright 2016-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import torch
from torch.utils.ffi import create_extension
this_dir = os.path.dirname(os.path.realpath(__file__))
torch_dir = os.path.dirname(torch.__file__)

print('Building SCN module')
if torch.cuda.is_available():
#    r = os.system(
#        'cd sparseconvnet/SCN; nvcc init.cu -c -o init.cu.o -ccbin /usr/bin/gcc-5'
#        + ' -m64 --std c++11 -Xcompiler '
#        + ',\"-fopenmp\",\"-fPIC\",\"-O3\",\"-DNDEBUG\" '
#        + '-gencode arch=compute_62,code=sm_62 '
#        + '-gencode arch=compute_61,code=sm_61 '
#        + '-gencode arch=compute_60,code=sm_60 '
#        + '-gencode arch=compute_52,code=sm_52 '
#        + '-gencode arch=compute_50,code=sm_50 '
#        + '-gencode arch=compute_30,code=sm_30 '
#        + '-DNVCC '
#        + '-I/opt/cuda/include '
#        + '-I' + torch_dir + '/lib/include '
#        + '-I' + torch_dir + '/lib/include/TH '
#        + '-I' + torch_dir + '/lib/include/THC '
#        + '-I.')
#    assert r == 0
    ffi = create_extension(
        'sparseconvnet.SCN',
        headers=[
            'sparseconvnet/SCN/header_cpu.h',
            'sparseconvnet/SCN/header_gpu.h'],
        sources=[],
        extra_objects=[
            this_dir +
            '/sparseconvnet/SCN/init.cu.o'],
        relative_to=__file__,
        include_dirs=['/opt/cuda/include'],
        with_cuda=True)
else:
    r = os.system(
        'cd sparseconvnet/SCN; g++-5 -std=c++11 -fPIC -c init.cpp -o init.cpp.o -I' +
        torch_dir +
        '/lib/include -I' +
        torch_dir +
        '/lib/include/TH -I.')
    assert r == 0
    ffi = create_extension(
        'sparseconvnet.SCN',
        headers=['sparseconvnet/SCN/header_cpu.h'],
        sources=[],
        extra_objects=[
            this_dir +
            '/sparseconvnet/SCN/init.cpp.o'],
        relative_to=__file__,
        with_cuda=False)

ffi.build()

from setuptools import setup, find_packages
setup(
    name='sparseconvnet',
    version='0.1.1',
    description='Submanifold (Spatially) Sparse Convolutional Networks https://arxiv.org/abs/1706.01307',
    author='Facebook AI Research',
    author_email='benjamingraham@fb.com',
    url='https://github.com/facebookresearch/SparseConvNet',
    package_data={
        'sparseconvnet': ['SCN/_SCN.so'],
    },
    packages=find_packages(),
    # Since the package includes a shared object, this is not zip-safe.
    zip_safe=False,
)
