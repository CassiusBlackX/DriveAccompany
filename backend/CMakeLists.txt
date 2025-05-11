project(yolo_detect)
cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(OpenCV_DIR /usr/local/opencv4.10.0)
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV Version: ${OpenCV_VERSION}")
message(STATUS "OpenCV Include: ${OpenCV_INCLUDE_DIRS}")

find_package(Crow REQUIRED)
message(STATUS "Crow VERSION: ${Crow_VERSION} ")

include_directories(${OpenCV_INCLUDE_DIRS})
add_executable(${PROJECT_NAME}_autobackup src/main.cpp src/yolo_detect.cpp src/base64.cpp src/utils.cpp)
target_compile_definitions(${PROJECT_NAME}_autobackup PRIVATE 
    CMAKE_LISTS_PATH="${CMAKE_CURRENT_SOURCE_DIR}"
)
target_link_libraries(${PROJECT_NAME}_autobackup ${OpenCV_LIBS} Crow::Crow pthread)