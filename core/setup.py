from setuptools import setup, find_packages

setup(
    name="data_core_app",
    version="0.1",
    packages=find_packages(),
    install_requires=['Django>=2.1'],
    package_data={'data_core_app': ['static/*.css', 'static/*.js', 'static/*.html', 'templates/*.html', 'static/*.xml',
                                    'static/*.json']},
    zip_safe=False
)