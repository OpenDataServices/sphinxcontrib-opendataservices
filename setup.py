from setuptools import setup

setup(
    name='sphinxcontrib-opendataservices',
    version='0.0.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    packages=['sphinxcontrib'],
    url='https://github.com/OpenDataServices/sphinxcontrib-opendataservices',
    install_requires=[
        'docutils',
        'jsonpointer',
        'recommonmark',
        'sphinx',
        'sphinxcontrib-opendataservices-jsonschema',
    ],
    extras_require={
        'test': [
            'coveralls',
            'flake8',
            'isort',
            'lxml',
            'myst-parser',
            'pytest',
            'pytest-cov',
        ],
    },
    namespace_packages=['sphinxcontrib'],
)
