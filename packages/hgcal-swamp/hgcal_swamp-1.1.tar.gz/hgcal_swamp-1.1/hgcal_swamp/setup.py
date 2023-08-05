from setuptools import setup, find_packages

setup(
    name='hgcal_swamp',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'transitions', 'PyYAML==6.0', 'pyjson==1.3.0',
        'nested_dict==1.61', 'tqdm'
    ],
)
