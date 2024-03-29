class Renderer():
    '''Render a return status, headers, and content as an HTTP response.'''
    def __init__(self, start_response):
        self.start_response = start_response

    def render_response(self, status, response_headers={}, response_body=''):
        '''Generate an HTTP response from status code and body.'''
        # remove hop-by-hop headers, which httplib doesn't like
        if 'transfer-encoding' in response_headers:
            del response_headers['transfer-encoding']

        response_headers = zip(*(response_headers.keys(), response_headers.values()))

        try:
            status = http_status[status]
        except KeyError:
            status = str(status) + ' UNKNOWN'

        self.start_response(status, response_headers)

        return [response_body]

http_status = {
    100: '100 CONTINUE',                      101: '101 SWITCHING PROTOCOLS',
    102: '102 PROCESSING',                    200: '200 OK',
    201: '201 CREATED',                       202: '202 ACCEPTED',
    203: '203 NON AUTHORITATIVE INFORMATION', 204: '204 NO CONTENT',
    205: '205 RESET CONTENT',                 206: '206 PARTIAL CONTENT',
    207: '207 MULTI STATUS',                  226: '226 IM USED',
    300: '300 MULTIPLE CHOICES',              301: '301 MOVED PERMANENTLY',
    302: '302 FOUND',                         303: '303 SEE OTHER',
    304: '304 NOT MODIFIED',                  305: '305 USE PROXY',
    307: '307 TEMPORARY REDIRECT',            400: '400 BAD REQUEST',
    401: '401 UNAUTHORIZED',                  402: '402 PAYMENT REQUIRED',
    403: '403 FORBIDDEN',                     404: '404 NOT FOUND',
    405: '405 METHOD NOT ALLOWED',            406: '406 NOT ACCEPTABLE',
    407: '407 PROXY AUTHENTICATION REQUIRED', 408: '408 REQUEST TIMEOUT',
    409: '409 CONFLICT',                      410: '410 GONE',
    411: '411 LENGTH REQUIRED',               412: '412 PRECONDITION FAILED',
    413: '413 REQUEST ENTITY TOO LARGE',      414: '414 REQUEST URI TOO LONG',
    415: '415 UNSUPPORTED MEDIA TYPE',        416: '416 REQUESTED RANGE NOT SATISFIABLE',
    417: '417 EXPECTATION FAILED',            422: '422 UNPROCESSABLE ENTITY',
    423: '423 LOCKED',                        424: '424 FAILED DEPENDENCY',
    426: '426 UPGRADE REQUIRED',              500: '500 INTERNAL SERVER ERROR',
    501: '501 NOT IMPLEMENTED',               502: '502 BAD GATEWAY',
    503: '503 SERVICE UNAVAILABLE',           504: '504 GATEWAY TIMEOUT',
    505: '505 HTTP VERSION NOT SUPPORTED',    507: '507 INSUFFICIENT STORAGE',
    510: '510 NOT EXTENDED'
}

