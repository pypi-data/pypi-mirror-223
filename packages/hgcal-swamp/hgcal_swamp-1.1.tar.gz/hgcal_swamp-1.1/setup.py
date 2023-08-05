from setuptools import setup, find_packages

setup(
    name='hgcal_swamp',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'transitions', 'PyYAML==6.0', 'pyjson==1.3.0',
        'nested_dict==1.61', 'tqdm'
    ],
    include_package_data=True
)
print(find_packages(include=['hgcal_swamp']))
