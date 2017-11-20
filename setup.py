from setuptools import setup

setup(
    name='sphinxcontrib-opendataservices',
    version='0.0.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    packages=['sphinxcontrib'],
    url='https://github.com/OpenDataServices/sphinxcontrib-opendataservices',
    install_requires=[
        'recommonmark',
        'jsonpointer',
        'Sphinx',
    ]
)
