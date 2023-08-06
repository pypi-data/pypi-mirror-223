# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nanox', 'nanox.model']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'nanox',
    'version': '0.1.1',
    'description': 'A transformer model for creating bio-compatible nanomachines',
    'long_description': 'None',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
