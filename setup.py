from setuptools import setup

setup(
    name='sphinxcontrib-opendataservices',
    version='0.6.0',
    author='Open Data Services',
    author_email='code@opendataservices.coop',
    packages=['sphinxcontrib'],
    url='https://github.com/OpenDataServices/sphinxcontrib-opendataservices',
    install_requires=[
        'docutils',
        'sphinx',
    ],
    extras_require={
        'test': [
            'coveralls',
            'flake8',
            'isort',
            'lxml',
            'pytest',
            'pytest-cov',
        ],
        'markdown': [
            'myst-parser',
        ],
        'json': [
            'jsonpointer',
            'sphinxcontrib-opendataservices-jsonschema>=0.5.0',
        ]
    },
    namespace_packages=['sphinxcontrib'],
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],
)
