from setuptools import setup, find_packages

setup(
    name='rbenchpoc',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'transformers',
        'bert-score',
        'pandas',
        'tqdm',
        'click',
    ],
)

