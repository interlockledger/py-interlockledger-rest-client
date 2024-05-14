DocumentsApi
============

The DocumentsApi allows you to insert document files (PDF, docx, text files,...) inside an IL2 chain.
To get an instance of the JsonApi, you can use the following example:

.. code-block:: python3
    

    from pyil2 import IL2Client
    
    client = IL2Client(
        host='https://il2.node:32032/',
        cert_filepath='rest.api.pfx',
        cert_password='Str0ngPassword'
    )
    api = client.api('documents')

The DocumentsApi is based on transactions to upload the files.
This way, it is possible to upload multiple files to a single record.
In summary, the basic steps to upload document files are as follows:

* Begin an upload transaction;

* Upload file;
    
    * Repeat for multiple files;

* Commit the upload transaction.

An example on how to upload document files to an IL2 chain:

.. code-block:: python3

    from pyil2.models.documents import BeginDocumentTransactionModel

    new_transaction = BeginDocumentTransactionModel(
        chain='UHtr...REDACTED...vXRY',
        comment='Additional comment to describe the files inside this record.',
        encryption='PBKDF2-SHA512-AES256-MID',
        password='1234567890123456'
    )
    transaction = api.begin_document_transaction(new_transaction)

    transaction = api.upload_document(
        transaction_id=transaction.transaction_id,
        filename='file1.txt',
        content_type='text/plain',
        file_bytes=b'Example 1',
        comment='Uploading a file using raw bytes as payload.'
    )

    transaction = api.upload_document_file(
        transaction_id=transaction.transaction_id,
        filepath='/path/to/file2.txt',
        comment='Uploading a file passing the file path.'
    )

    locator = api.commit_document_transaction(transaction.transaction_id)

After commiting the upload transaction, you will receive a locator to access the files inside the record.

.. note::
    The locator will be available only in the response to the transaction commit.
    It will not be possible to recover the locator afterward, store it in a safe location.

With the locator, it is possible to get the details of the files in the record, or download the files.

.. code-block:: python3

    metadata = api.get_document_metadata(locator)

    # Download a single file
    # This method will return the path to the downloaded file
    document_path = api.download_single_document_at(
        locator=locator, 
        index=0,
        dst_path='/path/to/download/folder'
    )

    # Download all files as a zip file
    # This method will return the path to the downloaded file
    document_path = api.download_documents_as_zip(
        locator=locator, 
        dst_path='/path/to/download/folder'
    )


The list of methods in the DOcumentsApi are described as follows:

.. autoclass:: pyil2.api.DocumentsApi
    :members:
    :show-inheritance: