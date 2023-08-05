# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfv', 'dfv.templatetags']

package_data = \
{'': ['*'], 'dfv': ['static/*', 'templates/dfv/tests/*']}

install_requires = \
['django-htmx>=1.14.0,<2.0.0',
 'django==4.2.4',
 'lxml>=4.9.2,<5.0.0',
 'typeguard',
 'wrapt>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'dfv',
    'version': '0.9.0',
    'description': 'Django Function Views',
    'long_description': 'None',
    'author': 'Roman Roelofsen',
    'author_email': 'romanroe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
