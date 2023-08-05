from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="risingwave",
    version="0.0.9",
    author="RisingWave Labs",
    description="RisingWave Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/risingwavelabs/risingwave",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires=">=3.8",
    install_requires=["pyarrow"],
    extras_require={"test": ["pytest"]},
)
