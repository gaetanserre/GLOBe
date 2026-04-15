cmake_minimum_required(VERSION 3.28)
project(optimizers)

# Detect platform
if(UNIX AND NOT APPLE)
  set(LINUX TRUE)
elseif(UNIX)
  set(DARWIN TRUE)
else()
  set(WINDOWS TRUE)
endif()

# ── Eigen ─────────────────────────────────────────────────────────────────────
find_package(Eigen3 REQUIRED NO_MODULE)

# ── libcmaes ──────────────────────────────────────────────────────────────────
set(LIBCMAES_BUILD_TESTS    OFF CACHE BOOL "" FORCE)
set(LIBCMAES_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(LIBCMAES_USE_OPENMP     OFF CACHE BOOL "" FORCE)
add_subdirectory(libcmaes ${CMAKE_BINARY_DIR}/libcmaes)

# ── GLPK ──────────────────────────────────────────────────────────────────────
file(GLOB_RECURSE GLPK_SRC_FILES glpk-5.0/src/*.c)
file(GLOB_RECURSE GLPK_HEADERS   glpk-5.0/src/*.h)

set(GLPK_INCLUDE_DIRS "")
foreach(hfile IN LISTS GLPK_HEADERS)
  get_filename_component(dir ${hfile} DIRECTORY)
  list(APPEND GLPK_INCLUDE_DIRS ${dir})
endforeach()
list(REMOVE_DUPLICATES GLPK_INCLUDE_DIRS)

add_library(glpk_obj SHARED ${GLPK_SRC_FILES})
set_target_properties(glpk_obj PROPERTIES LINKER_LANGUAGE C)
target_include_directories(glpk_obj PUBLIC ${GLPK_INCLUDE_DIRS})
target_compile_options(glpk_obj PRIVATE -O3 -fPIC -std=c99)

# ── Python ────────────────────────────────────────────────────────────────────
set(Python_EXECUTABLE "python" CACHE STRING "Path to the Python executable")
execute_process(
  COMMAND ${Python_EXECUTABLE} -c
    "from distutils.sysconfig import get_python_inc; print(get_python_inc())"
  OUTPUT_VARIABLE Python_INCLUDE_DIRS
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
set(Python_INCLUDE_DIRS ${Python_INCLUDE_DIRS} CACHE STRING "" FORCE)
message(STATUS "Python_EXECUTABLE:   ${Python_EXECUTABLE}")
message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")
message(STATUS "NUMPY_INCLUDE_DIRS:  ${NUMPY_INCLUDE_DIRS}")

# ── Sources ───────────────────────────────────────────────────────────────────
file(GLOB_RECURSE SRC_FILES src/*.cc src/*.cpp src/*.c)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(WINDOWS)
  set(CMAKE_CXX_FLAGS_RELEASE "/O2")
  find_package(Python COMPONENTS Development.Module REQUIRED)

  add_library(${EXT_NAME} SHARED ${SRC_FILES} ${CYTHON_CPP_FILE}
              $<TARGET_OBJECTS:glpk_obj>)
  target_include_directories(${EXT_NAME} PRIVATE
    include
    ${Python_INCLUDE_DIRS}
    ${NUMPY_INCLUDE_DIRS}
  )
  target_link_libraries(${EXT_NAME} PRIVATE
    Eigen3::Eigen
    cmaes
    glpk_obj
    ${Python_LIBRARIES}
  )
else()
  set(CMAKE_CXX_FLAGS "-fPIC -O3")

  add_library(${EXT_NAME} SHARED ${SRC_FILES} ${CYTHON_CPP_FILE}
              $<TARGET_OBJECTS:glpk_obj>)
  target_include_directories(${EXT_NAME} PRIVATE
    include
    ${Python_INCLUDE_DIRS}
    ${NUMPY_INCLUDE_DIRS}
  )
  target_link_libraries(${EXT_NAME} PRIVATE
    Eigen3::Eigen
    cmaes
    glpk_obj
  )
endif()

if(APPLE)
  set_target_properties(${EXT_NAME} PROPERTIES
    LINK_FLAGS "-undefined dynamic_lookup"
  )
endif()