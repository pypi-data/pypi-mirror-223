# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['txtadv',
 'txtadv.color',
 'txtadv.commands',
 'txtadv.file',
 'txtadv.location',
 'txtadv.messaging',
 'txtadv.wip.multiplayer']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2.17.0,<3.0.0']

setup_kwargs = {
    'name': 'txtadv',
    'version': '1.0',
    'description': 'A feature-rich text adventure library! Easy to code in and relativly intuitive, perfect for beginners!',
    'long_description': "# txtadv\n=======\ntxtadv is a feature-rich text adventure library! Easy to code in and relativly intuitive, perfect for beginners! Just install the library, with no dependencies other then the built-in libraries, for all computers.\nDocumentation is on it's way, I just wanted to get something out!",
    'author': 'sdft',
    'author_email': 'averse.abfun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11',
}


setup(**setup_kwargs)
