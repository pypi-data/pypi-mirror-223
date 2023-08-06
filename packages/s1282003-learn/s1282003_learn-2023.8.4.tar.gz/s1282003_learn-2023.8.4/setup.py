import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s1282003_learn",
    version="2023.08.04",
    author="Angelita Gozaly",
    author_email="s1282003@u-aizu.ac.jp",
    description="This software is being developed at the University of Aizu, Aizu-Wakamatsu, Fukushima, Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/angelitagozaly/s1282003_learn",
    license="GPLv3",
    install_requires=[
        "psutil",
        "pandas",
        "plotly",
        "matplotlib",
        "resource",
        "validators",
        "urllib3",
        "Pillow",
        "numpy",
        "pami",
    ],
    extras_require={
        "gpu": ["cupy", "pycuda"],
        "spark": ["pyspark"],
        "dev": ["twine", "setuptools", "build"],
        "all": ["cupy", "pycuda", "pyspark", "twine", "setuptools", "build"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
