from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='mrslpred',
    version='1.0',
    description='A tool to predict anti-bacterial peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/mrslpred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'mrslpred.blast_binaries':['**/*'], 
    'mrslpred.blast_db':['**/*'],
    'mrslpred.model':['*'],
    'mrslpred.motifs':['*'],
    'mrslpred.perl_scripts':['*']},
    entry_points={ 'console_scripts' : ['mrslpred = mrslpred.python_scripts.mrslpred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas', 'Bio', 'scikit-learn==1.0.2' , 'xgboost==0.90' # Add any Python dependencies here
    ]
)
