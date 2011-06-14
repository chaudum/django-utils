import os
from setuptools import setup, find_packages

setup_dict = dict(
    name = "rjdj.djangoutils",
    version = "0.1.2",
    author = 'Reality Jockey Limited',
    author_email = 'info@rjdj.me',
    description = 'Utility Package for Django and Tornado',
    url = 'http://rjdj.me',
	namespace_packages = ['rjdj'],
    packages = find_packages('src'),
    package_dir = {'':'src'},
    install_requires = ['distribute'],
    entry_points = {
        'console_scripts': [],
        },
    include_package_data = True,
    zip_safe = False,
    extras_require = dict(instance = [],
                          test = ['zope.testing','webtest','lxml',]),
)

setup(**setup_dict)

