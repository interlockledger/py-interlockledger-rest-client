RecordApi
=========

The RecordApi allows you to list, query and insert records in an IL2 chain.
To get an instance of the RecordApi, you can use the following example:

.. code-block:: python3
    
    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    api = client.api('record')

To list the records in a chain, you can use the code bellow:

.. code-block:: python3

    records = api.list_records('UHtr...REDACTED...vXRY')

It is also possible to make some queries using  the InterlockQL:

.. code-block:: python3

    # Query records that use the app 8 (JSON Documents)
    records = api.list_records(
        chain_id='UHtr...REDACTED...vXRY',
        query="USE APP #8\nEVERYTHING"
    )

It is also possible to insert records using the RecordApi, however, you will need to know the payload format in bytes for each app.
We highly recommend to use the APIs designed specifically for each application.

The list of methods are described as follows:

.. autoclass:: pyil2.api.RecordApi
    :members:
    :show-inheritance: