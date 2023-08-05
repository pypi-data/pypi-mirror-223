from setuptools import setup, find_packages

setup(
    name="yep_detectors",
    version="1.0.5",
    packages=find_packages(),
    install_requires=[
    ],
    data_files=[
        "decomp.jar"
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "yep_detector = yep_detector:main",
        ],
    },
)