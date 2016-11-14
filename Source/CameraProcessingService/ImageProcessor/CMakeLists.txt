cmake_minimum_required(VERSION 3.6)
project(cv_motion)

find_package( OpenCV 3 REQUIRED )

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

include_directories( ${OpenCV_INCLUDE_DIRS} )

set(SOURCE_FILES main.cpp)
add_executable(cv_motion ${SOURCE_FILES})
target_link_libraries( cv_motion ${OpenCV_LIBS} )
