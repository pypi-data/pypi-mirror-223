# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pose_labelbox']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0',
 'labelbox>=3.49.1',
 'pandas>=2.0',
 'python-slugify>=8.0.1',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.65.0',
 'wf-cv-utils>=3.6.0',
 'wf-honeycomb-io>=2.1.1',
 'wf-video-io>=3.4.2']

setup_kwargs = {
    'name': 'wf-pose-labelbox',
    'version': '0.2.0',
    'description': 'Tools for creating Labelbox projects involving 2D and 3D pose data',
    'long_description': '# pose_labelbox\n\nTools for creating Labelbox projects involving 2D and 3D pose data\n\n## Installation\n\n`pip install wf-pose-labelbox`\n\n## Development\n\n### Requirements\n\n* [Poetry](https://python-poetry.org/)\n* [just](https://github.com/casey/just)\n\n### Install\n\n`poetry install`\n\n\n#### Install w/ Python Version from PyEnv\n\n```\n# Specify pyenv python version\npyenv shell --unset\npyenv local <<VERSION>>\n\n# Set poetry python to pyenv version\npoetry env use $(pyenv which python)\npoetry cache clear . --all\npoetry install\n```\n\n## Task list\n* TBD\n',
    'author': 'Theodore Quinn',
    'author_email': 'ted.quinn@wildflowerschools.org',
    'maintainer': 'Theodore Quinn',
    'maintainer_email': 'ted.quinn@wildflowerschools.org',
    'url': 'https://github.com/WildflowerSchools/wf-pose-labelbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
