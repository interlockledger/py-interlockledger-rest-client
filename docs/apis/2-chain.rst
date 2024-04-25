ChainApi
========

.. code-block:: python3
    :linenos:

    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    chain_api = client.api('chain')

.. autoclass:: pyil2.api.ChainApi
    :members:
    :show-inheritance: