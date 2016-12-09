FROM python:3.5

RUN apt-get update \
	&& apt-get install -y unzip wget build-essential \
		cmake git pkg-config libswscale-dev \
		libtbb2 libtbb-dev libjpeg-dev \
        libpng-dev libtiff-dev libjasper-dev

RUN pip install numpy

RUN cd \
    && wget "https://github.com/Itseez/opencv/archive/3.1.0.zip" \
    && unzip "3.1.0.zip" \
    && cd "opencv-3.1.0" \
    && mkdir "build" \
    && cd "build" \
    && cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D BUILD_DOCS=OFF -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF \
        -D WITH_OPENCL=OFF -D WITH_CUDA=OFF .. \
    && make -j8 \
    && make install \
    && cd \
    && rm "3.1.0.zip" \
    && rm -rf "opencv-3.1.0"
