# -*- coding: utf-8 -*-
from setuptools import setup

packages = ['tronpy', 'tronpy.keys', 'tronpy.providers']

package_data = {'': ['*']}

install_requires = [
    'base58>=2.0.0,<3.0.0',
    'eth_abi>=2.1.1,<3.0.0',
    'pycryptodome>=3.9.7,<4.0.0',
    'requests>=2.23.0,<3.0.0',
]

setup_kwargs = {
    'name': 'nobi-tronpy',
    'version': '0.2.6',
    'description': 'TRON Python client library',
    'long_description': '''tronpy
======

TRON Python Client Library.
---------------------------

How to use
~~~~~~~~~~

.. code-block:: python

    from tronpy import Tron

    client = Tron(network='nile')
    # Private key of TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3
    priv_key = PrivateKey(bytes.fromhex("8888888888888888888888888888888888888888888888888888888888888888"))

    txn = (
        client.trx.transfer("TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3", "TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA", 1_000)
        .memo("test memo")
        .fee_limit(100_000_000)
        .build()
        .inspect()
        .sign(priv_key)
        .broadcast()
    )

    print(txn)
    # > {'result': True, 'txid': '5182b96bc0d74f416d6ba8e22380e5920d8627f8fb5ef5a6a11d4df030459132'}
    print(txn.wait())
    # > {'id': '5182b96bc0d74f416d6ba8e22380e5920d8627f8fb5ef5a6a11d4df030459132', 'blockNumber': 6415370, 'blockTimeStamp': 1591951155000, 'contractResult': [''], 'receipt': {'net_usage': 283}}
''',
    'author': 'andelf',
    'author_email': 'andelf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lovely-necromancer/tronpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
