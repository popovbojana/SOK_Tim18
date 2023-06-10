from setuptools import find_packages, setup

setup(
    name='xml_parser',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'source':
            ['load_xml=loading.loadData:LoadXML'],
    },
    zip_safe=True
)