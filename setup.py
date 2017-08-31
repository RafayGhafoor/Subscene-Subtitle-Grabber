from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import pypandoc

def readme():
    with open('README.rst', 'r') as f:
        return f.read()

setup(
    name='subgrab',
    version='0.2',
    description='A python script for automating subtitles downloading.',
    long_description=readme(),
    url='https://github.com/RafayGhafoor/sub-grab',
    author='Rafay Ghafoor',
    author_email='rafayghafoor@protonmail.com',
    packages=['subgrab', 'subgrab.source', 'subgrab.modules'],
    entry_points = {'console_scripts': ['subgrab = subgrab.__main__:main']},
    zip_safe = False,
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='subtitle automation subscene opensubtitles media',
    install_requires=['requests', 'bs4', 'lxml'],
)
