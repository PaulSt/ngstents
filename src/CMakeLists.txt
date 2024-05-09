cmake_minimum_required(VERSION 3.1)
project(ngstents)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find NGSolve and Netgen using python
if(CMAKE_VERSION VERSION_LESS "3.18")
  find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
else()
  find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
endif()
set(Netgen_DIR "" CACHE PATH "Path to directory containing NetgenConfig.cmake")
set(NGSolve_DIR "" CACHE PATH "Path to directory containing NGSolveConfig.cmake")
execute_process(COMMAND ${Python3_EXECUTABLE} -m netgen.config OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE Netgen_DIR)
execute_process(COMMAND ${Python3_EXECUTABLE} -m ngsolve.config OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NGSolve_DIR)
find_package(NGSolve CONFIG REQUIRED)

### check if CMAKE_INSTALL_PREFIX is set by user, if not install in NGSolve python dir
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    execute_process(COMMAND ${Python3_EXECUTABLE} -m site --user-site OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE install_dir RESULT_VARIABLE ret)
    if (NOT ret EQUAL 0)
        # user site directory is disabled (are we in a virtual environment?)
        set(install_dir ${Python3_SITEARCH})
    endif()
    message("The python module ${module_name} will be installed to: ${install_dir}")
    set(CMAKE_INSTALL_PREFIX ${install_dir} CACHE PATH "Install dir" FORCE)
else(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    #set(PY_INSTALL_DIR ${NGSOLVE_INSTALL_DIR_PYTHON} CACHE STRING "subdir of install dir for python modules")
    execute_process(COMMAND ${Python3_EXECUTABLE} -c "import os.path, sysconfig;print(os.path.relpath(sysconfig.get_path('platlib'), sysconfig.get_path('data')))" OUTPUT_VARIABLE PY_INSTALL_DIR OUTPUT_STRIP_TRAILING_WHITESPACE)
endif(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR} CACHE PATH "build dir")

add_library(_pytents SHARED
  python_tents.cpp
  tents.cpp
  )
add_library(_pyconslaw SHARED
  python_conslaw.cpp
  burgers.cpp
  euler.cpp
  wave.cpp
  advection.cpp
  maxwell.cpp
  symbolic.cpp
  vis3d.cpp
  )
target_link_libraries(_pytents PUBLIC ngsolve Python3::Module)
set_target_properties(_pytents PROPERTIES PREFIX "" CXX_STANDARD 17)
target_compile_definitions(_pytents PRIVATE NGSTENT_EXPORTS)
target_link_libraries(_pyconslaw PRIVATE _pytents)
set_target_properties(_pyconslaw PROPERTIES PREFIX "" CXX_STANDARD 17)
if(WIN32)
  set_target_properties(_pytents PROPERTIES SUFFIX ".pyd" )
  set_target_properties(_pyconslaw PROPERTIES SUFFIX ".pyd" )
else(WIN32)
  set_target_properties(_pytents PROPERTIES SUFFIX ".so")
  set_target_properties(_pyconslaw PROPERTIES SUFFIX ".so")
endif(WIN32)
set_target_properties(_pytents PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/ngstents")
set_target_properties(_pyconslaw PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/ngstents")

option(BUILD_STUB_FILES "Generate stub files for better autocompletion support" OFF)
if(BUILD_STUB_FILES)
  execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import pybind11_stubgen; print(pybind11_stubgen.__file__)" OUTPUT_VARIABLE stubgen_path RESULT_VARIABLE pybind11_stubgen)
  if(pybind11_stubgen AND NOT ${pybind11_stubgen} EQUAL 0)    
    message(WARNING "pybind11-stubgeN not found, if you want to create stub files
for better autocompletion support install it with pip.")
  else()
    message("-- Found pybind11-stubgen: ${stubgen_path}")
    set(FOUND_STUBGEN ON)
  endif()
   message(STATUS
      "This project is only compatible with\n\t\tpybind11-stubgen==0.5")
endif(BUILD_STUB_FILES)

message("With 'make install' the python package will be installed to: ${CMAKE_INSTALL_PREFIX}/${PY_INSTALL_DIR}")
install(TARGETS _pytents DESTINATION ${CMAKE_INSTALL_PREFIX}/${PY_INSTALL_DIR}/ngstents)
install(TARGETS _pyconslaw DESTINATION ${CMAKE_INSTALL_PREFIX}/${PY_INSTALL_DIR}/ngstents/conslaw)

install(FILES
  ../py/__init__.py
  DESTINATION ${CMAKE_INSTALL_PREFIX}/${PY_INSTALL_DIR}/ngstents)

install(FILES
  ../py/utils/__init__.py
  ../py/utils/_drawtents.py
  ../py/utils/_drawtents2d.py
  DESTINATION ${CMAKE_INSTALL_PREFIX}/${PY_INSTALL_DIR}/ngstents/utils)

install(FILES
  ../py/conslaw/__init__.py
  DESTINATION ${CMAKE_INSTALL_PREFIX}/${PY_INSTALL_DIR}/ngstents/conslaw)

if(FOUND_STUBGEN)
  install(CODE "execute_process(COMMAND ${PYTHON_EXECUTABLE} -m pybind11_stubgen --no-setup-py  ngstents)")
  install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/stubs/ngstents-stubs/ DESTINATION ${CMAKE_INSTALL_PREFIX}/${PY_INSTALL_DIR}/ngstents)
endif(FOUND_STUBGEN)
