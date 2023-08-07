from setuptools import setup, find_packages

# Same content as provided in the previous setup.py example

setup(
    name="pyecosystem",
    version="0.0.2",
    author="Smeet Kevadiya",
    author_email="",
    description="an ecosystem of various data transformers, structure builders, manipulators, workflows",
    long_description="an ecosystem of various data transformers, structure builders, manipulators, workflows",
    long_description_content_type="text/markdown",
    url="https://github.com/kevadiyasmt/pyecosystem",
    packages=find_packages(),
    classifiers=[
		'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'asyncio'
    ],
    python_requires=">=3.7",
)
