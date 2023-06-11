from distutils.core import setup
from setuptools import find_packages


setup(
    name="json_parser",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "source": ["load_json=load_json.data_loading:JsonDataLoader"],
    },
    zip_safe=False
)
