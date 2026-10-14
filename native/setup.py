from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "ecg_native",
        sources=[
            "src/module.cpp",
            "third_party/edflib/edflib.c",
        ],
        include_dirs=["third_party/edflib", "src"],
        cxx_std=17,
    ),
]

setup(
    name="ecg_native",
    version="0.1.0",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)