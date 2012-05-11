import httplib
import urllib
import re
import base64

class Resource():
    '''A convenvient wrapper for httplib.'''
    def __init__(self, url):
        '''connect to server based on standard-formatted url string'''
        match = re.match(r'((?P<protocol>.+):\/\/)?((?P<user>.+):(?P<pw>.+)?@)?(?P<host>.+?)(\/(?P<baseurl>[a-zA-Z0-9].+))?\/?$', url)
        if not match:
            raise ValueError('Error in URL string')

        self.protocol = match.group('protocol')
        self.host = match.group('host')
        self.base_url = match.group('baseurl')
        if self.base_url is None:
            self.base_url = ''

        self.headers = {}
        if match.group('user') and match.group('pw'):
            self.headers['Authorization'] = 'Basic %s' % base64.encodestring('%s:%s' % (match.group('user'), match.group('pw')))

    def connect(self):
        '''open an http(s) connection to this server'''
        if self.protocol == 'https':
            conn = httplib.HTTPSConnection(self.host)
        else:
            conn = httplib.HTTPConnection(self.host)
        return conn

    def request(self, method, url, body='', headers={}, **params):
        '''execute an http request to this server. params are built into the
        query string.
        '''
        # build headers and url
        all_headers = self.headers.copy()
        all_headers.update(headers or {})
        url = urljoin(self.base_url, url, **params)
        if not url.startswith('/'):
            url = '/' + url

        # make the request
        conn = self.connect()
        conn.request(method, url, body, all_headers)
        resp = conn.getresponse()

        # parse the response
        status = resp.status
        headers = dict(resp.getheaders())
        body = resp.read()
        return status, headers, body

    # HTTP methods
    def delete(self, path=None, headers=None, **params):
        return self.request('DELETE', path, headers=headers, **params)

    def head(self, path=None, headers=None, **params):
        return self.request('HEAD', path, headers=headers, **params)

    def get(self, path=None, headers=None, **params):
        return self.request('GET', path, headers=headers, **params)

    def put(self, path=None, body=None, headers=None, **params):
        return self.request('PUT', path, body=body, headers=headers, **params)

    def copy(self, path=None, body=None, headers=None, **params):
        return self.request('COPY', path, body=body, headers=headers, **params)

    def post(self, path=None, body=None, headers=None, **params):
        return self.request('POST', path, body=body, headers=headers, **params)

def urlencode(data):
    if isinstance(data, dict):
        data = data.items()
    params = []
    for name, value in data:
        params.append((name, value))
    return urllib.urlencode(params)

def urljoin(base, *path, **query):
    if base and base.endswith('/'):
        base = base[:-1]
    retval = [base]

    # build the path
    path = '/'.join([''] + [s for s in path])
    if path:
        retval.append(path)

    # build the query string
    params = []
    for name, value in query.items():
        if type(value) in (list, tuple):
            params.extend([(name, i) for i in value if i is not None])
        elif value is not None:
            if value is True:
                value = 'true'
            elif value is False:
                value = 'false'
            params.append((name, value))
    if params:
        retval.extend(['?', urlencode(params)])

    return ''.join(retval)

