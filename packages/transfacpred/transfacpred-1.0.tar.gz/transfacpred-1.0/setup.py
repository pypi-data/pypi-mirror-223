from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='transfacpred',
    version='1.0',
    description='A method to predict the transcription factors using protein sequences.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/transfacpred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'transfacpred.blastp':['**/*'], 
    'antibp3.blast_db':['**/*'],
    'antibp3.model':['*'],
    'antibp3.motif':['*'],
    'antibp3.perl_scripts':['*']},
    entry_points={ 'console_scripts' : ['antibp3 = antibp3.python_scripts.antibp3:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy == 1.21.5', 'pandas == 1.3.2', 'scikit-learn == 1.0.2'
    ]
)
