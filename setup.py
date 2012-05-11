from setuptools import setup

setup(
    name = 'woodstock',
    version = '0.7',
    description = 'resty rest',
    author = 'Andy Mastbaum',
    author_email = 'mastbaum@hep.upenn.com',
    url = 'http://github.com/mastbaum/woodstock',
    packages = ['woodstock'],
    scripts = ['bin/woodstock'],
    install_requires=['markdown']
)

