import contextlib
import tempfile
from typing import Any, Dict, List, Union
import requests
import urllib.parse
from base64 import b64encode
from .utils.certificates import PKCS12Certificate
from . import api
from .models.errors import ErrorDetailsModel

class IL2Client:
    """
     REST API client to the InterlockLedger node.

    You'll try to establish a bi-authenticated https connection with the 
    configured node API address and port. The client-side certificate used 
    to connect needs to be configured with the proper layered authorization 
    role in the node configuration file and imported into a key permitted to 
    update the chain that will be used. 

    Args:
        host (`str`): Host address in the format: scheme://hostmane[:port][/].
        cert_filepath (:obj:`str`): Path to the .pfx certificate. Please refer to the InterlockLedger manual to see how to create and import the certificate into the node.
        cert_password (:obj:`str`): Password of the .pfx certificate.
        verify_ca (`bool`): If `True`, verifies the SSL certificate in a CA (default: True).
        connect_timeout (:obj:`int`): Connect timeout in seconds (default: 5s).
        read_timeout (:obj:`int`): Read timeout in seconds (default 30s).
    """
    
    _available_apis = [
        'node',
        'chain',
        'record',
    ]
    
    def __init__(self, 
            host: str,
            cert_filepath: str,
            cert_password: str,
            verify_ca: bool=True,
            timeout:int = 30,
        ):
        self.host = host
        if self.host[-1] != '/':
            self.host += '/'
        self.verify_ca = verify_ca
        self.timeout = timeout
        self._session = None
        self._pem_file = None
        self.certificate = PKCS12Certificate(cert_filepath, cert_password)
        
    @property
    def public_certificate_in_x509(self):
        """:obj:`str`: Public certificate in X509 format."""
        x509 = (
            self.certificate.public_certificate
                .replace(b'-----BEGIN CERTIFICATE-----\n', b'')
                .replace(b'-----END CERTIFICATE-----\n', b'')
                .replace(b'\n', b'')
        )
        return x509
    
    @property
    def api_list(self) -> List[str]:
        """
        [:obj:`str`]: List of available APIs.
        """
        return self._available_apis

    def api(self, name: str) -> api.NodeApi | api.ChainApi | api.RecordApi | api.OpaqueApi:
        """
        Get an instance of an API.

        Args:
            name (:obj:`str`): API name.
        
        Returns:
            `BaseApi`: Instance of an API.
        """
        name = name.lower()
        match name:
            case 'node':
                return api.NodeApi(self)
            case 'chain':
                return api.ChainApi(self)
            case 'record':
                return api.RecordApi(self)
            case 'opaque':
                return api.OpaqueApi(self)
            case _:
                raise ValueError(f'No API with name {name} found. Must be in {self._available_apis}')
    
    def _get_session(self) -> requests.Session:
        if not self._session:
            self._pfx_to_pem()
            self._session = requests.Session()
            self._session.cert = self._pem_file.name
            self._session.verify = self.verify_ca
        return self._session

    @contextlib.contextmanager
    def _pfx_to_pem(self) -> None:
        self._pem_file = tempfile.NamedTemporaryFile(suffix='.pem')
        f_pem = open(self._pem_file.name, 'wb')
        f_pem.write(self.certificate.private_key)
        f_pem.write(self.certificate.public_certificate)
        f_pem.close()

    def __del__(self):
        if self._pem_file:
            self._pem_file.close()
        if self._session:
            self._session.close()

    def _join_uri(self, url: str):
        return urllib.parse.urljoin(self.host, url)

    def _prepare_headers(self, accept: str, content_type: str=None, auth: bool=True):
        headers = {
            'Accept':accept
        }
        if content_type:
            headers['Content-type'] = content_type
        return headers

    def _handle_error_response(self, response: requests.Response) -> requests.Response:
        try:
            if 400 <= response.status_code and response.status_code <= 599:
                return ErrorDetailsModel(**response.json())
        except Exception as exc:
            raise exc
        return response

    def _request(self, 
            url: str,
            method: str,
            accept: str='application/json',
            content_type: str='application/json',
            body: Dict[str, Any]=None, 
            params: Dict[str, str]={},
            auth: bool=True,
            data: bytes=None,
        ) -> requests.Response:
        method = method.upper()

        match method:
            case 'GET':
                resp = self._get(url=url, accept=accept, params=params, auth=auth)
            case 'DELETE':
                resp = self._delete(url=url, accept=accept, params=params, auth=auth)
            case 'POST':
                if data:
                    resp = self._post_data(url=url, accept=accept, content_type=content_type, data=data, auth=auth, params=params)
                else:
                    resp = self._post(url=url, accept=accept, content_type=content_type, body=body, auth=auth, params=params)
            case 'PATCH':
                resp = self._patch(url=url, accept=accept, content_type=content_type, body=body, auth=auth)
            case 'PUT':
                resp = self._put(url=url, accept=accept, content_type=content_type, body=body, auth=auth)
        
        return self._handle_error_response(resp)
    
    def _get(self, url: str, accept: str, params: Dict[str, str], auth: bool=True):
        cur_uri = self._join_uri(url)
        headers = self._prepare_headers(accept, auth=auth)
        response = self._get_session().get(
            cur_uri,
            headers=headers,
            params=params,
            timeout=self.timeout,
        )
        return response

    def _delete(self, url: str, accept: str, params: Dict[str, str], auth: bool=True):
        cur_uri = self._join_uri(url)
        headers = self._prepare_headers(accept, auth=auth)
        response = self._get_session().delete(
            cur_uri,
            headers=headers,
            params=params,
            timeout=self.timeout,
        )
        return response

    def _patch(self, url: str, accept: str, content_type: str, body: Dict[str, Any], auth: bool=True):
        cur_uri = self._join_uri(url)
        headers = self._prepare_headers(accept, content_type, auth=auth)
        response = self._get_session().patch(
            url=cur_uri,
            headers=headers,
            json=body,
            timeout=self.timeout,
        )
        return response
    
    def _put(self, url: str, accept: str, content_type: str, body: Dict[str, Any], auth: bool=True):
        cur_uri = self._join_uri(url)
        headers = self._prepare_headers(accept, content_type, auth=auth)
        response = self._get_session().put(
            url=cur_uri,
            headers=headers,
            json=body,
            timeout=self.timeout,
        )
        return response

    def _post(self, url: str, accept: str, content_type: str, body: Dict[str, Any], auth: bool=True, params: Dict[str, str]={}):
        cur_uri = self._join_uri(url)
        headers = self._prepare_headers(accept, content_type, auth=auth)
        response = self._get_session().post(
            url=cur_uri,
            headers=headers,
            json=body,
            params=params,
            timeout=self.timeout,
        )
        return response

    def _post_data(self, url: str, accept: str, content_type: str, data: bytes, auth: bool=True, params: Dict[str, str]={}):
        cur_uri = self._join_uri(url)
        headers = self._prepare_headers(accept, content_type, auth=auth)
        response = self._get_session().post(
            url=cur_uri,
            headers=headers,
            data=data,
            params=params,
            timeout=self.timeout,
        )
        return response


