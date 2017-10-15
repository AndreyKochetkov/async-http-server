import logging
import datetime
import os
import urllib.parse


class Parser:
    content_types = {
        'html': 'text/html',
        'css': 'text/css',
        'js': 'application/javascript',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'swf': 'application/x-shockwave-flash'
    }
    allowed_methods = ["GET", "HEAD"]
    default_page = 'index.html'
    default_encoding = 'utf-8'
    http_version = 'HTTP/1.1'
    server_name = "Andrey Kochetkov"

    ok = 200
    bad_request = 400
    forbidden = 403
    not_found = 404

    answer_codes = {
        200: 'OK',
        400: 'Bad Request',
        403: 'Forbidden',
        404: 'Not Found'
    }

    def __init__(self, request, static_dir, logger=None):
        self.request = request.decode()
        self.static_dir = static_dir
        self.logger = logger or logging.getLogger(__name__)

    def parse(self):
        self.request = self.request.splitlines()
        try:
            request_type, path, protocol = self.request[0].split(' ')
        except ValueError as e:
            self.logger.error(e)
            return self.get_response(code=self.bad_request)

        if request_type not in self.allowed_methods:
            self.logger.error("request_type not in allowed methods: {}".format(request_type))
            return self.get_response(code=self.bad_request)

        path = path.split('?')[0]
        path = urllib.parse.unquote(path)
        while '/' == path[0] and len(path) > 1:
            path = path[1:]

        if '../' in path:
            self.logger.error("'../' in path")
            return self.get_response(code=self.forbidden)

        whole_path = os.path.join(self.static_dir, path)
        if os.path.isdir(whole_path):
            whole_path = os.path.join(whole_path, self.default_page)
            if not os.path.exists(whole_path):
                return self.get_response(code=self.forbidden)

        if not os.path.exists(whole_path):
            self.logger.info("not found: {}".format(str(self.request)))
            return self.get_response(code=self.not_found)

        with open(whole_path, 'rb') as handle:
            file = handle.read()
        is_head = False
        if request_type == 'HEAD':
            is_head = True
        return self.get_response(code=self.ok, file=file, file_path=whole_path, is_head=is_head)

    def get_response(self, code, file=None, file_path=None, is_head=None):
        code_name = self.answer_codes.get(code)
        date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(file) if file else 0
        file = None if is_head else file
        try:
            expansion = file_path.rsplit('.').pop() if file_path else None
            type_ = self.content_types.get(expansion, 'application/octet-stream')
            content_type = type_ if file_path else 'application/octet-stream'

        except Exception as e:
            self.logger.error(e)
            return self.get_response(code=self.not_found)

        if code_name == "OK":
            file = file if file else b''
            return (
                       '{http_version} {code} {code_name}\r\n'
                       'Date: {date}\r\n'
                       'Server: {server_name}\r\n'
                       'Content-Length: {content_length}\r\n'
                       'Content-Type: {content_type}\r\n'
                       'Connection: keep-alive\r\n\r\n'
                   ).format(
                    http_version=self.http_version,
                    code=code,
                    code_name=code_name,
                    date=date,
                    server_name=self.server_name,
                    content_length=content_length,
                    content_type=content_type,
            ).encode() + file
        return (
            '{http_version} {code} {code_name}\r\n'
            'Date: {date}\r\n'
            'Server: {server_name}\r\n'
            'Connection: keep-alive\r\n\r\n'
        ).format(http_version=self.http_version,
                 code=code,
                 code_name=code_name,
                 date=date,
                 server_name=self.server_name,
                 ).encode()
