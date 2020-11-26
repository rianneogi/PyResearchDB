cmake_minimum_required(VERSION 2.6)

project(PopplerAPI)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

add_definitions(-DQT_NO_VERSION_TAGGING)

set(CMAKE_CXX_FLAGS "-Wall -Wextra -fPIC")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-g -Ofast -ffast-math -funroll-loops -flto -fwhole-program")
# set(CMAKE_EXE_LINKER_FLAGS "-pg -O3 -funsafe-math-optimizations")
# set(CMAKE_SHARED_LINKER_FLAGS "-pg -O3 -funsafe-math-optimizations")

SET(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/Bin)
# SET(CMAKE_BUILD_TYPE RELEASE)

# SET(PROJECT_SOURCE_DIR ${CMAKE_SOURCE_DIR}/Source)


## INCLUDE
include_directories("/usr/include/qt/")
include_directories("/usr/include/poppler/qt5/")

## TARGET
file(GLOB SOURCE_FILES
    Source/*.h
	Source/*.cpp
	*.cpp
	*.h
)

add_executable(PopplerAPI ${SOURCE_FILES})

## LINK
target_link_libraries(PopplerAPI ${Qt5Core_QTMAIN_LIBRARIES})