# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apis', 'apis.api', 'lib', 'lib.adapter']

package_data = \
{'': ['*']}

modules = \
['__init__', 'client']
install_requires = \
['bs4>=0.0.1', 'requests>=2.31']

setup_kwargs = {
    'name': 'feedancy',
    'version': '0.1.6',
    'description': 'сервис по сбору вакансий',
    'long_description': '# feedancy\n\nThe client is provided with async and sync adapters.\n\nTo install the async version with all its dependencies use:\n```bash\npip install feedancy[asyncio]\n```\n\nTo install the sync version with all its dependencies use:\n```bash\npip install feedancy[sync]\n```\n\nTo install both versions with all their dependencies use:\n```bash\npip install feedancy[asyncio,sync]\n```\n\n## Client instantiation example\n\n```python\n\nfrom feedancy import new_client, Configuration\nfrom feedancy.lib.adapter.requests import RequestsAdapter\n\nclient = new_client(RequestsAdapter(), Configuration(host="<your openapi server URL>"))\n```',
    'author': 'Alexey Ostanin',
    'author_email': 'aostaninn@gmal.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
