# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.0'


setup(
    name='pyfs-bot',
    version=version,
    keywords='Feishu Bot',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    url='https://github.com/feishu-sdk-python/pyfs-bot.git',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pyfs_bot'],
    py_modules=[],
    install_requires=['pyfs-base>=1.0.4'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
