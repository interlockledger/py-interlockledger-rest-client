ChainApi
========

The ChainApi is responsible to manage a chain in an IL2Node.
You will be able to see the list of chains in a node, create a new chain, manage the active IL2Apps in a chain, add permissions and force interlocks.
The following example shows how to get an instance of the ChainApi:

.. code-block:: python3
    

    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    api = client.api('chain')
    
    chains = api.list_chains()

If your are using a certificate with administration privileges, it is possible to create new chains:

.. code-block:: python3

    new_chain = ChainCreationModel(
        name="Chain name",
        emergency_closing_key_password="emergencyPassword",
        management_key_password="managementPassword",
    )

    created = api.create_chain(new_chain)

In case you need to permit new apps to this new chain, you can manage the permitted apps in the following way:

.. code-block:: python3
    
    permitted_apps = api.add_active_apps(
        new_chain.id,
        [4, 8]
    )

Now lets manage the permissions of the new chain in this node.
First we need to get the list of chains in the node and then we can change the permissions a key can have in this chain:

.. code-block:: python3
    
    from pyil2.models.keys import KeyDetailsModel

    chains = api.list_chains()
    key_to_permit = KeyDetailsModel(
        name='key.name',
        permissions=[
            '#2,500,501',
            '#1,300,301',
            '#5,701',
            '#3,601',
            '#4',
            '#8,2100'
        ],
        purposes=[
            'Action',
            'Protocol'
        ],
        id='Key!0ink...REDACTED...Ye2o#SHA1',
        public_key='PubKey!KPiQ...REDACTED...BAAE#RSA'
    )
    keys = api.add_keys(
        new_chain.id,
        keys_to_permit=[key_to_permit]
    )

.. note::
    To permit other keys, the certificate must be already imported to the Interlockledger node.

And finally, if you need to force an interlocking in a chain, you will need to follow the steps bellow:

.. code-block:: python3
    
    from pyil2.models.record import ForceInterlockModel
    
    interlock = ForceInterlockModel(
        target_chain='UHtr...REDACTED...vXRY'
    )
    response = api.force_interlocking(new_chain, interlock)
    


The list of methods in the ChainApi are described as follows:

.. autoclass:: pyil2.api.ChainApi
    :members:
    :show-inheritance: