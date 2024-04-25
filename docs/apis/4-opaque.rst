OpaqueApi
=========

The OpaqueApi allows you to insert records with an opaque payload to an IL2 chain.
The opaque payload allows you to insert any kind of data in raw bytes.
This way you can insert an arbitrary object using your own data format.
To get an instance of the OpaqueApi, you can use the following example:

.. code-block:: python3
    

    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    api = client.api('opaque')

Although each application in IL2 has its own identification by an integer number.
The opaque record allows you to use any application ID.
If your application requires different types of payload, you can use different codes for each type by using the payload_type_id to identify the different payloads.
In summary, the opaque record allows you to use IL2 as your application need.
To insert an opaque record, you can use the following method:

.. code-block:: python3

    opaque = api.add_opaque(
        chain_id='UHtr...REDACTED...vXRY',
        application_id=123,
        payload_type_id=1234,
        payload=b'mydata'
    )

To retrieve an opaque record you just use the following:

.. code-block:: python3

    opaque = api.get_opaque(
        chain_id='UHtr...REDACTED...vXRY', 
        serial=42
    )
    # my_custom_deserializer is your function to deserialize the payload
    my_object = my_custom_deserializer(opaque.payload)


The list of methods are described as follows:

.. autoclass:: pyil2.api.OpaqueApi
    :members:
    :show-inheritance: