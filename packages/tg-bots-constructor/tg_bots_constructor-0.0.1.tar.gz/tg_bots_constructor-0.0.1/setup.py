from setuptools import setup

version = '0.0.1'


setup(
    name='tg_bots_constructor',
    version=version,

    author='morpheus228',
    author_email='tabunovbai@gmail.com',

    description=(
        "Constructor for telegram bots, based on aiogram library"
    ),

    url='https://github.com/morpheus228/tg_bots_constructor.git',

    download_url='https://github.com/morpheus228/tg_bots_constructor.git/archive/main.zip',

    # license='Apache License, Version 2.0, see LICENSE file',

    packages=['tg_bots_constructor'],
    install_requires=['aiogram==3.0.0b8']

    #     classifiers=[
    #     'License :: OSI Approved :: Apache Software License',
    #     'Operating System :: OS Independent',
    #     'Intended Audience :: End Users/Desktop',
    #     'Intended Audience :: Developers',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.6',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: Implementation :: PyPy',
    #     'Programming Language :: Python :: Implementation :: CPython',
    # ]
)  