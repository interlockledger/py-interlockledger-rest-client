NodeApi
=======

The NodeApi is responsible to make the requests regarding details about the node.
You can check the detailed information about an IL2 node, list the peers and more.
The following example shows how to get an instance of the NodeApi:

.. code-block:: python3
    
    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    node_api = client.api('node')
    
    print(node_api.details.name)

The list of methods are described as follows:

.. autoclass:: pyil2.api.NodeApi
    :members:
    :show-inheritance: