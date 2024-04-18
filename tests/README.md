# How to run the unittests

The unit tests for the client uses a real instance of an IL2 node.
Thus it is needed to configure some settings to properly run the tests.

## Before running the tests

Before running the tests, you will need to set some environment variables to configure the IL2 node details. See `.env.sample` for more details. You will need to set the following environment variables:

```bash
TEST_CERTIFICATE_PATH=path/to/api/certificate.pfx
TEST_CERTIFICATE_PASS=client_password
TEST_HOST=https://node.il2:32032
TEST_DEFAULT_CHAIN=default_test_chain_id
TEST_SECOND_CHAIN=default_secundary_chain_id_to_interlock
TEST_CERTIFICATE_ENCRYPTED_IV=api_certificate_encrypted_iv
TEST_CERTIFICATE_ENCRYPTED_KEY=api_certificate_encrypted_key
TEST_CERTIFICATE_PUBLIC_KEY_HASH=api_certificate_public_key_hash
TEST_CERTIFICATE_READER_ID=api_certificate_reader_id
TEST_CERTIFICATE_2_PATH=path/to/invalid/reading/key/certificate.pfx
TEST_CERTIFICATE_2_PASS=invalid_certificate_password
TEST_CIPHER_TEXT=base64_json_encrypted_with_api_certificate
```

You can check the description of each variable bellow:

| Environment Variable               | Description                                                                                           | Example                                            |
| :--------------------------------- | :---------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `TEST_CERTIFICATE_PATH`            | Path to a PFX certificate with permissions in an IL2 node.                                            | /home/user/rest.api.pfx                            |
| `TEST_CERTIFICATE_PASS`            | Password to open the certificate.                                                                     | Str0ngPassword                                     |
| `TEST_HOST`                        | Address to the IL2 node to be used in the test.                                                       | https://node.il2.io:32032/                         |
| `TEST_DEFAULT_CHAIN`               | Default chain ID to be used in the tests.                                                             | kFa9icqyCAtql1DNZEenFHQfDgk8AC1z-gmxm53i5BY        |
| `TEST_SECOND_CHAIN`                | A secondary chain ID to be used int the tests                                                         | wZMENHbComADN_eXZ9WkSS-S_cCsONZbO4wg9VajYGQ        |
| `TEST_CERTIFICATE_ENCRYPTED_IV`    | Value of an AES IV. (see the reading keys in a JSON record as example)                                | tkiCsd2fClfSnypMP+d/P0v...(REDACTED)...jAGF/hR5QB  |
| `TEST_CERTIFICATE_ENCRYPTED_KEY`   | Value of an AES key. (see the reading keys in a JSON record as example)                               | PTb+LFnX6+sEXQYz...(REDACTED)...CcV2ZgS4b9yc5YF    |
| `TEST_CERTIFICATE_PUBLIC_KEY_HASH` | Public key hash in IL2 text representation. (see the reading keys in a JSON record as example)        | I0Nqvj72zUqAc851IpB3M_gGrpVoHIgAdIYAfw4Rl1Q#SHA256 |
| `TEST_CERTIFICATE_READER_ID`       | Id of the key in IL2 text representation. (see the reading keys in a JSON record as example)          | Key!vgkXGQobsHqkkc6azd1F3_6WBXw#SHA1               |
| `TEST_CERTIFICATE_2_PATH`          | Path to a second certificate to be used in the JSON document encryption tests.                        | /home/user/another.pfx                             |
| `TEST_CERTIFICATE_2_PASS`          | Password to open the second certificate.                                                              | NotSoStrongPassword                                |
| `TEST_CIPHER_TEXT`                 | An encrypted JSON document encrypted and decoded in base64. (see the cipher text in an JSON document) | BZRTve9fCRxbN6aJ/wWZuLGf3vfC1zcvhekC7G42miA=       |

> **NOTE**: For the variables related to the JSON documents tests. We highly recommend to add an encrypted JSON document and using the values of the encrypted text and the reading keys in that JSON document record.(see the reading keys in a JSON record as example)

## Running the tests

We are using a the standard Python `unittest` package. To run the tests use the following command in the project root folder:

```console
$ python -m unittest
```
