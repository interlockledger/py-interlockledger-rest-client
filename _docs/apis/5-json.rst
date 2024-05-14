JsonApi
=======

The JsonApi allows you to insert records with an arbitrary JSON payload.
The JSON payload will be encrypted and it will only be possible to decode the payload if you have the correct key.
By default, the payload will be encrypted using the key used to insert the JSON payload, but it is possible to insert a JSON payload with different reading keys.
To get an instance of the JsonApi, you can use the following example:

.. code-block:: python3
    

    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    api = client.api('json')

To insert a JSON encrypted with the certificate used to insert the JSON:

.. code-block:: python3

    payload = {
        'attr': 'value'
    }
    json_doc = api.add_json_document(
        chain_id='UHtr...REDACTED...vXRY',
        payload=payload
    )
    serial = json_doc.serial

To get a JSON record and to decode the JSON payload:

.. code-block:: python3

    json_doc = api.get_json_document(
        chain_id='UHtr...REDACTED...vXRY',
        serial=serial
    )

    decrypted = json_doc.encrypted_json.decode(client.certificate)

As stated earlier, you can store a JSON with a secondary reading key.
The reading key needs to be in the IL2 format.
Currently, the pyil2 client only supports PKCS12 certificates (PFX files), so you can use another PKCS12 certificate to add another reading key.

.. code-block:: python3

    fom pyil2.utils.certificates import PKCS12Certificate

    certificate_2 = PKCS12Certificate('certificate_2.pfx', 'Str0ngerPassword')

    payload = {
        'attr': 'value'
    }
    json_doc = self.api.add_json_document_with_key(
        chain_id='UHtr...REDACTED...vXRY',
        payload=payload,
        public_key=certificate_2.pub_key, 
        public_key_id=certificate_2.key_id
    )

The decodification process is the same as before but using `certificate_2` instead of `client.certificate`.

If you need multiples reading keys, you can insert a record with a list of allowed reading keys:

.. code-block:: python3

    from pyil2.models.json import (
        AllowedReadersModel,
        ReaderKeyModel
    )

    allowed_readers = AllowedReadersModel(
        contextId='allowed_readers_list_name',
        readers=[
            ReaderKeyModel(
                name=certificate_2.key_id,
                public_key=certificate_2.pub_key
            )
        ]
    )
    
    reference = api.allow_json_document_readers(
        chain_id='UHtr...REDACTED...vXRY',
        allowed_readers=allowed_readers
    )

With a list of allowed reading keys inserted, we can now insert a JSON document with more reading keys:

.. code-block:: python3

    payload = {
        'attr': 'value'
    }
    json_doc = api.add_json_document_with_indirect_keys(
        chain_id='UHtr...REDACTED...vXRY',
        payload=payload,
        keys_references=[reference],
    )

.. note::
    You can use more than one allowed reading keys record reference.

Finally, you can also insert a JSON document record with all reading keys allowed in one chain:

.. code-block:: python3

    payload = {
        'attr': 'value'
    }
    json_doc = api.add_json_document_with_chain_keys(
        chain_id='UHtr...REDACTED...vXRY',
        payload=payload,
        keys_chain_id=['ArFj...REDACTED...bHxP'],
    )

The list of methods in the JsonApi are described as follows:

.. autoclass:: pyil2.api.JsonApi
    :members:
    :show-inheritance: