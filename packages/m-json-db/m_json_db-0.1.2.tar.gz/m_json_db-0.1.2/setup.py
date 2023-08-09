# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['m_json_db']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'm-json-db',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'megahomyak',
    'author_email': 'g.megahomyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
