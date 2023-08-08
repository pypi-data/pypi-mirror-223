# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dubo']

package_data = \
{'': ['*']}

install_requires = \
['altair>=5.0.1,<6.0.0', 'pandas>=1.0.0,<2.0.0', 'pydeck>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'dubo',
    'version': '0.2.5',
    'description': 'Analytics made simple',
    'long_description': 'dubo\n====\n\ndubo is a client for running LLMs against DataFrames and other 2D data.\n\nIt is currently in an alpha release and not yet ready for use in production pipelines.\n',
    'author': 'Andrew Duberstein',
    'author_email': 'ajduberstein@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
