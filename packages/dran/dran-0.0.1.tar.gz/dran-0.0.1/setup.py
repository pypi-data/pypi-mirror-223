from setuptools import setup

# include readme file
with open("README.md", "r") as f:
    long_description= f.read()

setup(
    name="dran", # can be different
    version='0.0.1', # 0.0.x implies this is an unstable version
    description="Data reduction and analysis of HartRAO 26m telescope drift scans",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["dran"], # the modules we're importing
    package_dir={'':'src'}, # the package we're installing
    url="https://github.com/Pfesi/dran", # update once you have a release
    author="Pfesesani van Zyl",
    author_email="pfesi24@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Operating System :: OS Independent"
    ],

    # dependencies, if you change this re-run install
    # install_requires = [

    #                     ]

    # development requirements
    # pip install -e .[dev]
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ]
    }
)