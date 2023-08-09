# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coca_websocket']

package_data = \
{'': ['*']}

install_requires = \
['websockets>=11.0.3,<12.0.0']

setup_kwargs = {
    'name': 'coca-websocket',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Hiroyuki Ikuno',
    'author_email': 'sam2kaikaramegusuri@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CocaButon60s/coca_websocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
