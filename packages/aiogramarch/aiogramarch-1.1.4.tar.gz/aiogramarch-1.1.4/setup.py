# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogramarch',
 'aiogramarch.arch',
 'aiogramarch.cli',
 'aiogramarch.cli.templates',
 'aiogramarch.cli.templates.app',
 'aiogramarch.cli.templates.app.{{ cookiecutter.app_name }}',
 'aiogramarch.cli.templates.project',
 'aiogramarch.cli.templates.project.{{ cookiecutter.project_name }}',
 'aiogramarch.cli.templates.project.{{ cookiecutter.project_name }}.src']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=3.0.0b',
 'click>=8.1.3',
 'cookiecutter>=2.1.1',
 'loguru>=0.6.0',
 'pydantic==1.10.12']

entry_points = \
{'console_scripts': ['aiogramarch = aiogramarch.cli.app:cli']}

setup_kwargs = {
    'name': 'aiogramarch',
    'version': '1.1.4',
    'description': 'Managing aiogram projects',
    'long_description': '# <p align="center"> Aiogramarch </p>\nProject manager and generator for Aiogram\n\n\n\n___\n\n## Installation\n\n``` python\npip install aiogram-manager\n```\n___\n\n## How to use\n\n``` bash\naiogram startproject [projectname]\n```\n\n``` bash\ncd codingbot\n```\n\n``` bash\naiogram startapp [appname]\n```\n\n___\n\n## Utils options\n\n``` bash\naiogram --help\n```\n',
    'author': 'BulatXam',
    'author_email': 'Khamdbulat@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
