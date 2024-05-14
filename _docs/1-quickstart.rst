Quickstart
==========

This quickstart tutorial will show how to use the IL2 Python Client.
In this tutorial you will learn the basics of the IL2 client and how to make some operations.

.. note::
    To connect to an IL2 node, you will need to use an permissioned certificate (a PFX file).
    This certificate must be already imported to the IL2 node and have the correct permissions to the chains.


The Basics
----------

To start using the IL2 client, you will need to create an instance of the IL2Client.
The instance of the IL2Client will access one IL2 node host using a PFX certificate.
After creating the IL2Client, you will need to get an API requests set.
With the API instance you will be able to list the chains in the node, add records and more.
Each operation will depend on the API requests set.

The following example shows how to instantiate the IL2Client and see the list of available APIs:

.. code-block:: python3
    

    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    print(client.api_list)

With IL2Client, we can indicate which API we want to use.
Let's get the list of chains in this node and store the ID of the first chain:

.. code-block:: python3
    

    chain_api = client.api('chain')
    chains = chain_api.list_chains()
    chain_id = chains[0].id
    print(chain_id)

Since we have a chain ID, let's store an encrypted JSON in this chain:

.. code-block:: python3
    
    
    json_api = client.api('json')
    encrypted_json = json_api.add_json_document(
        chain_id,
        {
            'attribute': "value"
        }
    )

The other operations work the same way, you will need to indicate the API you need and then use the required request.