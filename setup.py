from setuptools import setup, find_packages
from codecs import open
from os import path

version = '0.1.0'
here = path.abspath(path.dirname(__file__))
read_me = path.join(here, 'README.rst')

# Get the long description from the README file
with open(read_me, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CsCntlr',
    version=version,
    description='A python package for the color sensor S11059-02DT',
    long_description=long_description,
    # The project's main homepage
    url='https://github.com/NariseT/CsCntlr',
    author='Takafumi Narise',
    author_email='narise.pub@gmail.com',
    license='MIT',

    classifiers=[
        # Development Status
        'Development Status :: 3 - Alpha',
        
        # Environment (Raspbian Console)
        'Environment :: Console',
        'Operating System :: Other OS',
        
        # Indicate Audience, Topic
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # License
        'License :: OSI Approved :: MIT License',

        # Supported Python versions
        'Programming Language :: Python :: 2.7',
    ],

    keywords='Color-sensor S11059-02DT Raspberry-Pi',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=['smbus'],
    
)
