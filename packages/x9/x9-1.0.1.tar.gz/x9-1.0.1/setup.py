from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="x9",
    version="1.0.1",
    author="PyModuleDev",
    author_email="pxcom@mail.com",
    description="X9 is a user-friendly multi-use module made by PyModuleDev.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["x9"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.1"
)
