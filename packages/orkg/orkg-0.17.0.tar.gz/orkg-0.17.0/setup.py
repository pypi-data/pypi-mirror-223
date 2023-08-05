# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orkg',
 'orkg.client',
 'orkg.client.harvesters',
 'orkg.client.templates',
 'orkg.graph']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.14,<2.0.0',
 'Faker>=19.1.0,<20.0.0',
 'Inflector>=3.1.0,<4.0.0',
 'cardinality>=0.1.1,<0.2.0',
 'hammock>=0.2.4,<0.3.0',
 'networkx>=3.1,<4.0',
 'pandas>=2.0.1,<3.0.0',
 'pydantic>=2.0.3,<3.0.0',
 'requests>=2.31.0,<3.0.0',
 'tqdm>=4.65.0,<5.0.0',
 'undecorated>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'orkg',
    'version': '0.17.0',
    'description': 'The official python client for the Open Research Knowledge Graph (ORKG) API',
    'long_description': '# orkg-pypi\n[![pipeline status](https://gitlab.com/TIBHannover/orkg/orkg-pypi/badges/main/pipeline.svg)](https://gitlab.com/TIBHannover/orkg/orkg-pypi/-/commits/master)\n[![Documentation Status](https://readthedocs.org/projects/orkg/badge/?version=latest)](https://orkg.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/orkg.svg)](https://badge.fury.io/py/orkg)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n[![flake8](https://img.shields.io/badge/flake8-enabled-brightgreen)](https://github.com/PyCQA/flake8)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nA python client interacting with the ORKG API and sprinkling some python magic on top.\n\nThe package a implements many of the API calls described in the [documentation](http://tibhannover.gitlab.io/orkg/orkg-backend/api-doc/), and provides a set of extra features like graph pythonic objects and dynamic instantiation of entities from specifications.\n\nYou can find details about how-to use the package on [Read the Docs](https://orkg.readthedocs.io/en/latest/index.html).\n\nDevelopers, please note that you need to install the pre-commit script via\n```bash\npip install -r requirements.txt\npre-commit install\n```\nAnd check the [CONTRIBUTING.md](CONTRIBUTING.md) for more details.\n\n# Noteworthy Contributors\n\nSpecial thanks to the following awesome people\n- Allard Oelen\n- Kheir Eddine Farfar\n- Omar Arab Oghli\n- Julia Evans\n',
    'author': 'Yaser Jaradeh',
    'author_email': 'yaser.jaradeh@tib.eu',
    'maintainer': 'Yaser Jaradeh',
    'maintainer_email': None,
    'url': 'http://orkg.org/about',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
