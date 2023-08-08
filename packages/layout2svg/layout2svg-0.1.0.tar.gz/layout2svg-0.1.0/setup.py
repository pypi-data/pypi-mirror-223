# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['layout2svg']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0',
 'colour>=0.1.5,<0.2.0',
 'docopt>=0.6.2,<0.7.0',
 'gdstk>=0.9.42,<0.10.0',
 'klayout>=0.28.10,<0.29.0',
 'loguru>=0.7.0,<0.8.0',
 'lxml>=4.9.3,<5.0.0']

entry_points = \
{'console_scripts': ['layout2svg = bin.layout2svg:main']}

setup_kwargs = {
    'name': 'layout2svg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dasdias',
    'author_email': 'das.dias6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
