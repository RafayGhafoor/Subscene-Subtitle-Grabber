from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='subgrab',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1',

    description='A python script for automating subtitles downloading.',
    # The project's main homepage.
    url='https://github.com/RafayGhafoor/sub-grab',

    # Author details
    author='Rafay Ghafoor',
    author_email='rafayghafoor@protonmail.com',
    packages=['subgrab', 'subgrab.source'],
    entry_points = {'console_scripts': ['subgrab = subgrab.__main__:main']},
    zip_safe = False,
    # Choose your license
    license='GPL',

    python_requires='2.7',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='subtitle automation subscene opensubtitles media',

    install_requires=['requests', 'bs4', 'lxml'],
)
