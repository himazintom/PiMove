cmake_minimum_required(VERSION 3.20)
project(CPictureModifier)

add_subdirectory(pybind11)
pybind11_add_module(CPictureModifier CPictureModifier.cpp)
