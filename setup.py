import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nodal",
    version="0.0.1",
    author="Michael Thingnes",
    author_email="thimic@gmail.com",
    description="An execution graph for Python tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thimic/nodal",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    setup_requires=['wheel'],
)
