from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='il5pred',
    version='1.0',
    description='A tool to predict il5 inducing peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/il5pred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'il5pred.blast_binaries':['**/*'], 
    'il5pred.blast_db':['**/*'],
    'il5pred.model':['*']},
    entry_points={ 'console_scripts' : ['il5pred = il5pred.python_scripts.il5pred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas',  # Add any Python dependencies here
    ]
)
