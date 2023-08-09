# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['layout3mesh']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0',
 'gdstk>=0.9.42,<0.10.0',
 'mapbox-earcut>=1.0.1,<2.0.0',
 'scipy>=1.11.1,<2.0.0',
 'shapely>=2.0.1,<3.0.0',
 'trimesh>=3.23.1,<4.0.0']

entry_points = \
{'console_scripts': ['layout2svg = layout2svg.cli:main']}

setup_kwargs = {
    'name': 'layout3mesh',
    'version': '0.1.0',
    'description': 'A tool to generate 3D meshes from 2D integrated circuit layouts',
    'long_description': '<h1 align=center> layout3mesh </h1>\n\n<div align=justify>\n<p> This is a simple tool to convert an integrated circuit layout saved in OASIS / GDSII file format to a mesh 3D image file. The tool supports direct export of the 3D mesh file into the Blender desktop app. This tool was written with the goal of rendering any layout in 3D inside a desktop or web application using WebGL. </p>\n</div>\n\n<h2 align=center> Installation </h2>\n\n<h3 align=center> MacOS, Linux, Windows </h3>\n\n```bash\npip install layout3mesh\n```\n\n<h2 align=center> Usage - Command Line Interface </h2>\n\n```bash\nlayout3mesh -i <input_file_path [.gds/.oas]> -o <output_file_path [.gltf]> -t <layerstack_file_path [.ymls]>\n```\n\n<h2 align=center> Examples </h2>\n\n<p>\nRunning the example with the mock layerstack file and layout provided in the <a href="tests/data/">examples</a>, by running the following command:\n</p>\n\n```bash\nlayout3mesh -i ./tests/data/crossed_metal.gds -t ./tests/data/mock_layers.ymls -o ./tests/data/crossed_metal.gltf\n```\n\n<p>\ncan generate the following 3D image:\n</p>\n\n<p align=center>\n\n\n<img src="tests/data/crossed_metal.gif" width=70%/>\n\n</p>\n',
    'author': 'dasdias',
    'author_email': 'das.dias6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/das-dias/layout3mesh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
