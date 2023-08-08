# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantix_genai_inference',
 'semantix_genai_inference.inference',
 'semantix_genai_inference.inference.llm']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'click>=8.1.4,<9.0.0']

entry_points = \
{'console_scripts': ['semantix-ai = semantix_genai_inference.cli:cli']}

setup_kwargs = {
    'name': 'semantix-genai-inference',
    'version': '0.0.1',
    'description': '',
    'long_description': "# Semantix GenAI Inference\n\nA python client library to help you interact with the Semantix GenAI Inference API.\n\n\n# Installation\n\nIf you're using pip, just install it from the latest release:\n\n    $ pip install semantix-genai-inference\n\nElse if you want to run local, clone this repository and install it with poetry:\n\n    $ poetry build\n    $ poetry install\n\n# Usage\n\nTo use it:\n\n    $ semantix-ai --help\n\n",
    'author': 'Your Name',
    'author_email': 'you@example.com',
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
