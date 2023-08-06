from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='exopropred',
    version='1.0',
    description='A tool to predict the subcellular localisation of exosomal proteins',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/exopropred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'exopropred.blast_binaries':['**/*'],
    'exopropred.Data':['*'],
    'exopropred.extra':['*'],
    'exopropred.model':['*'],
    'exopropred.motif':['*'],
    'exopropred.perl_scripts':['*'],
    'exopropred.swissprot':['*']},
    entry_points={'console_scripts' : ['exopropred = exopropred.python_scripts.exopropred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas', 'argparse', 'scikit-learn'# Add any Python dependencies here
    ]
)
