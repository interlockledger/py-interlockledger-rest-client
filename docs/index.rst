.. IL2 Rest Client documentation master file, created by
   sphinx-quickstart on Tue Apr 23 16:21:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

IL2 Python Client
=================

.. image:: /images/full-logo.svg
    :width: 400
    :align: center

This package is a Python client to the InterlockLedger Node REST API.
It connects to InterlockLedger nodes, allowing the creation of chains, interlocks, and storage of records and documents.

The InterlockLedger
-------------------

An `InterlockLedger <https://il2.io/>`_ network is a peer-to-peer network of nodes.
Each node runs the InterlockLedger software.
All communication between nodes is point-to-point and digitally signed, but not mandatorily encrypted.
This means that data is shared either publicly or on a need-to-know basis, depending on the application.

In the InterlockLedger, the ledger is composed of myriads of independently permissioned chains, comprised of blockchained records of data, under the control of their owners, but that are tied by Interlockings, that avoid them having their content/history being rewritten even by their owners.
For each network the ledger is the sum of all chains in the participating nodes. 

A chain is a sequential list of records, back chained with signatures/hashes to the previous records, so that no changes in them can go undetected.
A record is tied to some enabled InterlockLedgerApplication (IL2App), that defines the metadata associate with it.
The IL2App defines the constraints of a record as a public metadata, stored in the network genesis chain.

How to use
----------

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    0-installation
    1-quickstart
    2-apis

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
