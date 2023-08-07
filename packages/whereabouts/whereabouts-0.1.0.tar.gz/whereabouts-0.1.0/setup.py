# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whereabouts']

package_data = \
{'': ['*']}

install_requires = \
['duckdb==0.7.1',
 'fastparquet>=2023.7.0,<2024.0.0',
 'lxml>=4.9.2,<5.0.0',
 'openpyxl>=3.1.1,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyarrow>=12.0.1,<13.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'scipy>=1.11.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'whereabouts',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Whereabouts\nFast, scalable geocoding for Python using an embedded database\n\n## Description\nGeocode addresses and reverse geocode coordinates with a simple, fast package. No additional database setup required. Currently only working for Australian data.\n\n## Requirements\n- Python 3.8+\n- Poetry (for package management)\n\n## Installation\nOnce Poetry is installed and you are in the project directory:\n\n```\npoetry shell\npoetry install\n```\n\nDownload the latest version of the GNAF\n```\npython download_gnaf.py\n```\n\nAnd setup the geocoder. This creates the required reference tables, etc.\n```\npython setup_geocoder.py\n```\n\n## Examples\n',
    'author': 'alex2718',
    'author_email': 'ajlee3141@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)
