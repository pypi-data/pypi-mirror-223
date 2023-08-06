# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyuri']

package_data = \
{'': ['*']}

install_requires = \
['hstspreload>=2023.1.1,<2024.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'easyuri',
    'version': '0.1.3',
    'description': 'a dumb URL parser with a smart interface',
    'long_description': '`easyuri` is a dumb URL parser with a smart interface.\n\n    >>> import easyuri\n    >>> uri = easyuri.parse("en.wikipedia.org/wiki/Jabberwocky")\n    >>> uri.is_secure, uri.in_hsts\n    (True, True)\n    >>> uri.scheme, uri.host, uri.port\n    (\'https\', \'en.wikipedia.org\', 443)\n    >>> uri.subdomain, uri.domain, uri.suffix, uri.path\n    (\'en\', \'wikipedia\', \'org\', \'wiki/Jabberwocky\')\n    >>> str(uri)\n    \'https://en.wikipedia.org/wiki/Jabberwocky\'\n\n    >>> uri = easyuri.parse("http://evil.com\\\\@good.com/")  # doctest: +IGNORE_EXCEPTION_DETAIL\n    Traceback (most recent call last):\n    ...\n    DifficultURLError\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/easyuri',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
