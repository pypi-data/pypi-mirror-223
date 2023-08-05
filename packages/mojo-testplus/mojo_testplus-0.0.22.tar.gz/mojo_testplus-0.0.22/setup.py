# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo',
 'mojo.factories',
 'mojo.testplus',
 'mojo.testplus.cli',
 'mojo.testplus.cli.cmdtree',
 'mojo.testplus.cli.cmdtree.testing',
 'mojo.testplus.cli.cmdtree.utilities',
 'mojo.testplus.registration',
 'mojo.testplus.templates']

package_data = \
{'': ['*'], 'mojo.testplus.templates': ['static/v0/*', 'tabs/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'debugpy>=1.6.5,<2.0.0',
 'mojo-runtime>=0.0.52,<0.1.0',
 'mojo-xmodules>=0.0.64,<0.1.0',
 'requests<=2.29.0']

extras_require = \
{'couchdb': ['couchdb>=1.2,<2.0'],
 'interop': ['mojo-interop>=0.0.21,<0.1.0'],
 'mongodb': ['pymongo[srv]>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'mojo-testplus',
    'version': '0.0.22',
    'description': 'Automation Mojo TestPlus Test Framework',
    'long_description': "==========================\nAutomation Mojo - Testplus\n==========================\n \nThis is preliminary release of the 'testplus' automation framework in a separate package from\nthe AutomationKit.  This release is not ready for public consumption.\n\n",
    'author': 'Myron Walker',
    'author_email': 'myron.walker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://automationmojo.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
