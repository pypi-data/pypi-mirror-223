import random_word_numpy
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="random_word_numpy",
    version="0.0.2",
    author="Ben Schreck <ben@benschreck.com>",
    author_email="ben@benschreck.com",
    description="This is a simple python package to generate random english words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="package random words word of the day random word generator",
    url="https://github.com/bschreck/random-word-numpy",
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['pytest-runner'],
    tests_require=["pytest"],
    install_requires=["requests", "pytest", "pyyaml"],
    include_package_data=True,
    zip_safe=False,
)
