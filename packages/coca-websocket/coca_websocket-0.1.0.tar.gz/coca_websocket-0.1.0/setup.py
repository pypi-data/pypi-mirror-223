# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coca_websocket']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coca-websocket',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Hiroyuki Ikuno',
    'author_email': 'sam2kaikaramegusuri@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
