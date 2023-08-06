# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['non_iid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'non-iid',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Christine',
    'author_email': 'cdonnelly0626@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
