# InterlockLedger REST Client in Python

This package is a python client to the InterlockLedger Node REST API. It connects to InterlockLedger nodes, allowing the creation of chains, interlocks, and storage of records and documents.

This library replaces the original client, 
[interlockledger-rest-client-python](https://github.com/interlockledger/interlockledger-rest-client-python),
that is now deprecated.

## The InterlockLedger

An InterlockLedger network is a peer-to-peer network of nodes. Each node runs the InterlockLedger software. All communication between nodes is point-to-point and digitally signed, but not mandatorily encrypted. This means that data is shared either publicly or on a need-to-know basis, depending on the application.

In the InterlockLedger, the ledger is composed of myriads of independently permissioned chains, comprised of blockchained records of data, under the control of their owners, but that are tied by Interlockings, that avoid them having their content/history being rewritten even by their owners. For each network the ledger is the sum of all chains in the participating nodes.

A chain is a sequential list of records, back chained with signatures/hashes to the previous records, so that no changes in them can go undetected. A record is tied to some enabled Application, that defines the metadata associate with it, and the constraints defined in this public metadata, forcibly stored in the network genesis chain, is akin to validation that each correct implementation of the node software is able to enforce, but more
importantly, any external logic can validate the multiple dimensions of validity for records/chains/interlockings/the ledger.

## Dependencies

-   Python 3.11.3

    -   pydantic 2.6.1
    -   requests 2.31.0
    -   pyOpenSSL 24.1.0
    -   pyilint 0.2.2
    -   pyiltags 0.1.1

-   InterlockLedger:
    -   API 14.0.0

## Example

How to use the interlockledger rest client. This example will show how to list the chains in a node and store an encrypted JSON document in the first chain:

```python
from pyil2 import IL2Client

client = IL2Client(
    host='https://il2.node:32032/',
    cert_filepath='rest.api.pfx',
    cert_password='Str0ngPassword'
)

chain_api = client.api('chain')
chains = chain_api.list_chains()
chain_id = chains[0].id

json_api = client.api('json')
encrypted_json = json_api.add_json_document(
    chain_id,
    {
        'attribute': "value"
    }
)
```

## License

This program is licensed under the **BSD 3-Clause License**.

## Contributions

We are not actively looking for contributions but if you want to help, feel free
to do so via the [project's gitHub page](https://github.com/interlockledger/py-interlockledger-rest-client).

