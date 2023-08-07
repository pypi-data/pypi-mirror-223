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
    'version': '0.1.1',
    'description': 'Terminal Piano App',
    'long_description': '# UPiano\n\nA Piano in your terminal.\n\n\n## Screenshot\n\n ![](./screenshot-upiano.png)\n\n\n## How to run\n\nInstall via pip:\n\n    pip install upiano\n\nAnd then run:\n\n    upiano\n\nMake sure your terminal window is big enough.\nThe wider you can make it, the more keys you\'ll have! 🎹 😀\n\n\n## Powered by\n\n* [Python](https://www.python.org) 🐍\n* [Textual](https://textual.textualize.io/)\n* [FluidSynth](https://github.com/FluidSynth/fluidsynth)\n* [pyFluidSynth](https://github.com/nwhitehead/pyfluidsynth)\n\nMade with ❤️  by Elias Dorneles\n\n\n## History\n\nThis started as a fun pairing project by friends\n[Elias](https://github.com/eliasdorneles) and\n[Nandaja](https://github.com/nandajavarma) around 2017, after they had\nfinished their [Recurse Center](https://recurse.com) retreat and were missing\nhacking together.\n\nThey had fun building a small terminal piano app using\n[urwid](https://urwid.org) for the user interface and playing notes by spawning\n[sox](https://sox.sourceforge.net) subprocesses. This version is available in\nthe project source code, if you have urwid and sox installed, you can try it by\nrunning: `python upiano/legacy.py`.\n\nFast-forward to 2023, Elias attended EuroPython and learned the\n[Textual](https://textual.textualize.io) library there, got excited about\nterminal apps again and decided to reboot this project using the newly acquired\nknowledge, package and distribute it, and add to the fun by plugging a true\nsynthesizer to it, and playing with its controls.\n\n\n### Changelog:\n\n* **v0.1.0**\n    * first version released to PyPI, already using Textual\n* **v0.1.1**\n    * added sustain\n    * fix mouse handling, and allow playing by "swiping" over keys\n',
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
