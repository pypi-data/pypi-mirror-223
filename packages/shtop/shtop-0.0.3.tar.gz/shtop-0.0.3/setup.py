from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Simple tui slurm job viewer.'

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "Readme.md").read_text()

# Setting up
setup(
        name="shtop", 
        version=VERSION,
        author="Lukáš Plevač",
        author_email="<lukas@plevac.eu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 

        scripts=['scripts/shtop'],

        keywords=['python', 'slurm', 'shtop', 'top', 'htop'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3"
        ]
)
