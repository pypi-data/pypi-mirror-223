# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hogwarts',
 'hogwarts.magic_urls',
 'hogwarts.management',
 'hogwarts.management.commands',
 'hogwarts.migrations',
 'hogwarts.tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.2.2,<5.0.0', 'rich>=13.5.2,<14.0.0', 'ruff>=0.0.280,<0.0.281']

setup_kwargs = {
    'name': 'django-hogwarts',
    'version': '0.1.0',
    'description': 'Django utilities for codegen and DX improvement',
    'long_description': None,
    'author': 'adiletto64',
    'author_email': 'adiletdj19@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
