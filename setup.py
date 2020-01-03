# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='mcloud',
    version='0.1.0',
    author='Marius Stanca',
    author_email='me@marius.xyz',
    url='http://mariuss.me',
    license='MIT',
    description='Manage cloud resources.',
    py_modules=['mcloud'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        mcloud=mcloud:cli
    ''',
    classifiers=[
        'Environment :: Tools Environment',
        'Intended Audience :: sys ops',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6.1',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
