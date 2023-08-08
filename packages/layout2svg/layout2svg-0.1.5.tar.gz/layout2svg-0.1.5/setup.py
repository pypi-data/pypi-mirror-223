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
{'console_scripts': ['layout2svg = layout2svg.cli:main']}

setup_kwargs = {
    'name': 'layout2svg',
    'version': '0.1.5',
    'description': 'A package to convert IC layouts (GDS2 and OASIS) to SVG.',
    'long_description': '<h1 align=center> layout2svg </h1>\n\n<div align=justify>\n<p> This is a simple tool to convert an integrated circuit layout saved in OASIS / GDSII file format to a .SVG image file. The tool supports direct export of the SVG file into the Inkscape desktop app. This tool was written with the goal of rendering any layout in a desktop or web application. </p>\n</div>\n\n<h2 align=center> Installation </h2>\n\n<h3 align=center> MacOS, Linux, Windows </h3>\n\n```bash\npip install layout2svg\n```\n\n<h2 align=center> Usage - Command Line Interface </h2>\n\n```bash\nlayout2svg -i <input_file_path [.gds/.oas]> -o <output_file_path [.svg]>\n```\n\n<h2 align=center> Examples </h2>\n\n<p>\nRunning the example with the mock layerstack file and layout provided in the <a href="tests/data/">examples</a>, by running the following command:\n</p>\n\n```bash\nlayout2svg -i examples/crossed_metal.gds -t examples/mock_layers.lys.yml -o examples/crossed_metal.svg\n```\n\n<p>\ncan generate the following SVG image:\n</p>\n\n<p align=center>\n\n\n<img src="tests/data/crossed_metal.png" width=400/>\n\n\n</p>\n',
    'author': 'dasdias',
    'author_email': 'das.dias6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/das-dias/layout2svg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
