# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['timestreams']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'timestreams',
    'version': '0.0.1a1',
    'description': 'A placeholder for a future kaskada project',
    'long_description': '# Kaskada Timestreams\n\n## Developer Instructions\nThe package uses Poetry to develop and build.\n\n1. Install Pyenv [Pyenv Documentation](https://github.com/pyenv/pyenv)\n1. Install Python 3.9.16: `$ pyenv install 3.9.16`\n1. Install Poetry [Poetry Documentation](https://python-poetry.org/docs/)\n1. Install dependences: `$ poetry install`\n\n#### Build the Package\nTo build the client: `$ poetry build`\n\n#### Publishing the Package to PyPi\n* build the package (see above)\n* set the POETRY_PYPI_TOKEN_PYPI env var in your environment\n* from the `./clients` folder:, run `$ docker compose run push-timestreams`\n',
    'author': 'Kaskada',
    'author_email': 'maintainers@kaskada.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
