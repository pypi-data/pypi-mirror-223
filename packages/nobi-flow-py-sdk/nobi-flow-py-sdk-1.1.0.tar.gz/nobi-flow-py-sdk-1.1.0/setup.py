# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow_py_sdk',
 'flow_py_sdk.cadence',
 'flow_py_sdk.client',
 'flow_py_sdk.frlp',
 'flow_py_sdk.proto',
 'flow_py_sdk.proto.flow',
 'flow_py_sdk.signer',
 'flow_py_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['betterproto[compiler]>=1.2.5,<2.0.0',
 'ecdsa>=v0.17.0',
 'phe>=1.4.0',
 'grpcio-tools>=1.33.2,<2.0.0',
 'grpclib>=0.4.1,<0.5.0',
 'rlp>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['examples = examples.main:run']}

setup_kwargs = {
    'name': 'nobi-flow-py-sdk',
    'version': '1.1.0',
    'description': 'A python SKD for the flow blockchain',
    'long_description': '''Flow Python SDK
===============

The Flow Python SDK provides a comprehensive set of packages for Python developers, enabling them to create applications that seamlessly interact with the Flow network.

.. image:: https://img.shields.io/pypi/v/flow-py-sdk.svg
   :target: https://pypi.org/project/flow-py-sdk/
   :alt: PyPI Version

.. image:: https://codecov.io/gh/janezpodhostnik/flow-py-sdk/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/codecov/example-go
   :alt: Code Coverage

For a detailed guide, visit the official documentation: `Flow Python SDK Guide <https://janezpodhostnik.github.io/flow-py-sdk>`_.

This SDK is fully compatible with the Flow Emulator, making it ideal for local development.

Installation
------------

To start using the SDK, ensure you have Python 3.9 or higher installed, and then install the package:

Using pip::

    pip install flow-py-sdk

Using poetry::

    poetry add flow-py-sdk

Contributors
------------

Check out our contributors on `GitHub Contributors <https://github.com/janezpodhostnik/flow-py-sdk/graphs/contributors>`_.

Made with `contrib.rocks <https://contrib.rocks>`_.
''',
    'author': 'Janez Podhostnik',
    'author_email': 'janez.podhostnik@gmail.com',
    'maintainer': 'Abolfazl Bakiasay, Milad EbrahimKhani',
    'maintainer_email': 'abolfazl850@gmail.com, milade3013@gmail.com',
    'url': 'https://github.com/milade3013/flow-py-sdk-python3.8',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
