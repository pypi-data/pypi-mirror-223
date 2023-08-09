# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amhelpers']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.3,<3.0.0', 'scikit-learn>=1.3.0,<2.0.0']

extras_require = \
{':python_version >= "3.9" and python_version < "4.0"': ['numpy>=1.25.2,<2.0.0']}

setup_kwargs = {
    'name': 'amhelpers',
    'version': '0.4.0',
    'description': 'A collection of handy utilities.',
    'long_description': '# amhelpers\n\nA collection of handy utilities.\n\n## Installation\n\n```bash\n$ pip install amhelpers\n```\n\n## License\n\n`amhelpers` was created by Anton Matsson. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`amhelpers` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Anton Matsson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
