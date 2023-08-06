# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upiano']

package_data = \
{'': ['*'], 'upiano': ['soundfonts/*']}

install_requires = \
['pyFluidSynth>=1.3.2,<2.0.0', 'textual>=0.32.0,<0.33.0']

entry_points = \
{'console_scripts': ['upiano = upiano.app:main']}

setup_kwargs = {
    'name': 'upiano',
    'version': '0.1.0',
    'description': 'Terminal Piano App',
    'long_description': '# UPiano\n\nA Piano in your terminal.\n\nPowered by:\n\n* [Python](https://www.python.org)\n* [Textual](https://textual.textualize.io/)\n* [FluidSynth](https://github.com/FluidSynth/fluidsynth)\n* [pyFluidSynth](https://github.com/nwhitehead/pyfluidsynth)\n\nMade with ❤️  by Elias Dorneles\n',
    'author': 'Elias Dorneles',
    'author_email': 'elias.dorneles@hey.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
