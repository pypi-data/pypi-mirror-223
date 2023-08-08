from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='phagetb',
    version='1.0',
    description='A multilevel prediction method for predicting interactions between bacteriophages and pathogenic bacterial hosts',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/phagetb', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'phagetb.base':['**/*'],
    'phagetb.blast_binaries':['**/*'],
    'exopropred.tmp':['*']},
    entry_points={'console_scripts' : ['phagetb = phagetb.python_scripts.model:main', 'phagetb_1 = phagetb.python_scripts.model_bacteria:main',
                                       'phagetb_2 = phagetb.python_scripts.model_phage_host_pair:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas','argparse', 'scikit-learn' # Add any Python dependencies here
    ]
)
