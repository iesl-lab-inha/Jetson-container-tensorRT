FROM nvcr.io/nvidia/l4t-base:r32.3.1
WORKDIR /
RUN apt update && apt install -y --fix-missing make g++ pkg-config
RUN apt install -y --fix-missing python3-pip hdf5-tools protobuf-compiler
RUN apt install -y --fix-missing libhdf5-serial-dev libhdf5-dev zlib1g-dev zip


ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/hdf5/serial
RUN pip3 install -U pip Cython
RUN pip3 install -U future==0.17.1 mock==3.0.5 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 numpy==1.16.1  enum34 futures protobuf
RUN pip3 install -U h5py
RUN pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 'tensorflow-gpu==1.15'

RUN apt update && apt install --fix-missing -y build-essential cmake git libgtk2.0-dev pkg-config libswscale-dev python3-dev python3-numpy

COPY /Driver_Profiling /profile

EXPOSE 5600
CMD ["/bin/bash"]
