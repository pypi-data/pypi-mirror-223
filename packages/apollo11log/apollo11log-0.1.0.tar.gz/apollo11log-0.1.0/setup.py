# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apollo11log']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['apollo11log = apollo11log:__main__.main']}

setup_kwargs = {
    'name': 'apollo11log',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'xss',
    'author_email': 'michaela@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xssfox/apollo11log',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
