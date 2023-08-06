#!/usr/bin/env python3
# coding: utf-8
'''
Author: biao.li <biao.li@flexiv.com>
'''
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name='newpychromedriver',
    # TODO: sync version with Chrome Driver
    version=version,
    author='biao.li',
    author_email='biao.li@flexiv.com',
    description='A package to sync chrome driver to lastest version',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/parklam/newpychromedriver',
    #packages=setuptools.find_packages(),
    packages=['newpychromedriver'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    keywords='chromedriver chrome driver',
)
