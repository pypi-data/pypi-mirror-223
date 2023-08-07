from setuptools import setup, find_packages

# Same content as provided in the previous setup.py example

setup(
    name="pyecosystem",
    version="0.0.1",
    author="Smeet Kevadiya",
    author_email="",
    description="an ecosystem of various data transformers, structure builders, manipulators, workflows",
    long_description="an ecosystem of various data transformers, structure builders, manipulators, workflows",
    long_description_content_type="text/markdown",
    url="https://github.com/kevadiyasmt/ecosystem",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # List any dependencies here
    ],
    python_requires=">=3.7",
)
