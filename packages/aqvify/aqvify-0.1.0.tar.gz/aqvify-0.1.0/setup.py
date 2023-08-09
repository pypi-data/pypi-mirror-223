""" Setup for python-aqvify """

from setuptools import setup

setup(
    name='aqvify',
    version='0.1.0',
    description='Read values from Aqvify through the official API.',
    long_description='A python module for reading values of Aqvify through the official API.',
    url='http://github.com/ptz0n/python-aqvify',
    author='Erik Eng',
    author_email='erik@eng.se',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='home automation aqvify',
    setup_requires=['wheel'],
    install_requires=['requests'],
    packages=['aqvify'],
    zip_safe=True
)
