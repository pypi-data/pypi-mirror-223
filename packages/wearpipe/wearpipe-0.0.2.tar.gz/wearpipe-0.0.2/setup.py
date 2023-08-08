from setuptools import setup, find_packages

setup(
    name='wearpipe',
    version='0.0.2',
    url='https://github.com/chags1313/wearpipe',
    author='Cole Hagen',
    author_email='hagencolej@gmail.com',
    description='Python package that enables fast wearable data pipeline executation from data preprocessing to model application',
    packages=find_packages(),    
    install_requires=[
       'numpy',
       'pandas',
       'sklearn',
       'tensorflow'
    ],
 )