from setuptools import find_packages, setup

setup(
    name='visualisation_simple',
    version='0.1',
    packages=find_packages(),
    package_data={'simpleVisual': ['templates/*.html']},
    entry_points={
        'visualisation':
            ['load_json=simpleVisual.simpleVisual:SimpleVisualisation'],
    },
    zip_safe=False
)
