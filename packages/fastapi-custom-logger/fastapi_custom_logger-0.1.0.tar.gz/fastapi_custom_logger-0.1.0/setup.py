# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastapi_custom_logger']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.79.0,<0.80.0', 'loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'fastapi-custom-logger',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Dominik Bucko',
    'author_email': 'domminik.bucko@pan-net.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
