from setuptools import find_packages, setup

setup(
    name='visualisation_complex',
    version='0.1',
    packages=find_packages(),
    package_data={'complex': ['templates/*.html']},
    entry_points={
        'visualisation':
            ['load_xml=complex.visualisation_complex:VisualisationComplex'],
    },
    zip_safe=False
)