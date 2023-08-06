from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cdpred',
    version='1.1',
    description='A tool to predict celiac disease associated peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://gitlab.com/raghavalab/cdpred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'cdpred.Model':['*']},
    entry_points={ 'console_scripts' : ['cdpred = cdpred.Python_scripts.cdpred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas', 'scikit-learn==1.2.2'# Add any Python dependencies here
    ]
)
