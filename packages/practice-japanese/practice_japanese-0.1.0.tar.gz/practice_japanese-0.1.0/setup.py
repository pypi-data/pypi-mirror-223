from setuptools import setup, find_packages
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, "README.md")) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, "practice_japanese", "version.py")) as f:
    exec(f.read(), version)

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="practice_japanese",
    version=version["__version__"],
    description="Practice Japanese character sets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Heather Ward",
    author_email="heather.ward13@gmail.com",
    url="https://github.com/hkeward/practice_japanese",
    license="gpl-2.0",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": ["practice_japanese=practice_japanese.command_line:cli"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: Unix",
    ],
)
