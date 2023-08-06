from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='toxinpred3',
    version='1.4',
    description='A tool to predict toxic and non-toxic peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/toxinpred3', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={ 'toxinpred3.model':['*'],
    'toxinpred3.motifs':['*'],
    'toxinpred3.merci':['*']},
    entry_points={ 'console_scripts' : ['toxinpred3 = toxinpred3.python_scripts.toxinpred3:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas' , 'argparse', 'joblib' # Add any Python dependencies here
    ]
)
