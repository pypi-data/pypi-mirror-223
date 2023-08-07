# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shear_psf_leakage']

package_data = \
{'': ['*']}

install_requires = \
['TreeCorr>=4.3.3,<5.0.0',
 'cs-util>=0.0.4,<0.0.5',
 'lmfit>=1.2.2,<2.0.0',
 'matplotlib>=3.7.2,<4.0.0',
 'uncertainties>=3.1.7,<4.0.0']

entry_points = \
{'console_scripts': ['leakage_object = shear_psf_leakage.leakage_object:main',
                     'leakage_scale = shear_psf_leakage.leakage_scale:main']}

setup_kwargs = {
    'name': 'shear-psf-leakage',
    'version': '0.1.0',
    'description': 'PSF leakage for shear catalogue data',
    'long_description': '',
    'author': 'Martin Kilbinger',
    'author_email': 'martin.kilbinger@cea.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
