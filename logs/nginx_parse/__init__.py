"""
What we're expecting, from nginx config (see: ../vagrant/ansible/roles/open-notify-webserver/meta/main.yml):

log_format apilog '$msec | $remote_addr $status $request_time $upstream_response_time $upstream_cache_status $body_bytes_sent | "$scheme $request" "$http_user_agent"'

"""
import datetime


DEBUG = False


class Request(object):

    def __init__(
        self,
        msec,
        datetime,
        remote_addr,
        status,
        request_time,
        upstream_response_time,
        upstream_cache_status,
        body_bytes_sent,
        scheme,
        request,
        http_verb,
        request_path,
        protocol,
        http_user_agent
    ):
        self.msec = msec
        self.datetime = datetime
        self.remote_addr = remote_addr
        self.status = status
        self.request_time = request_time
        self.upstream_response_time = upstream_response_time
        self.upstream_cache_status = upstream_cache_status
        self.body_bytes_sent = body_bytes_sent
        self.scheme = scheme
        self.request = request
        self.http_verb = http_verb
        self.request_path = request_path
        self.protocol = protocol
        self.http_user_agent = http_user_agent

        # Figure out tags based on request_path:
        self.endpoint_tag = "unknown"
        if 'iss-now' in self.request_path:
            self.endpoint_tag = "iss-now"
        elif 'iss-pass' in self.request_path or '/iss/' in self.request_path:
            self.endpoint_tag = "iss-pass"
        elif 'astro' in self.request_path:
            self.endpoint_tag = "astros"
        elif self.request_path == '/' or 'index.html' in self.request_path:
            self.endpoint_tag = "index"

    def __repr__(self):
        return "<nginx_parse.Request {}>".format(self.msec)


def parseline(line):

    line_parts = line.split()
    if DEBUG:
        print(line_parts)

    # $msec is a unix timestamp down to milisecond resolution
    msec = float(line_parts[0])
    date = datetime.datetime.utcfromtimestamp(msec)
    if DEBUG:
        print('$msec:                   ', msec)
        print('datetime:                ', date)

    # $remote_addr is the IP that started the request
    remote_addr = line_parts[2]
    if DEBUG:
        print('$remote_addr:            ', remote_addr)

    # $status is the HTTP status code replied to this request
    status = int(line_parts[3])
    if DEBUG:
        print('$status:                 ', status)

    # $request_time is the total time spent handling the request
    request_time = float(line_parts[4])
    if DEBUG:
        print('$request_time:           ', request_time)

    # $upstream_response_time is the time we spent getting the data from the backend
    upstream_response_time = line_parts[5]
    try:
        upstream_response_time = float(upstream_response_time)
    except ValueError:
        upstream_response_time = None
    if DEBUG:
        print('$upstream_response_time: ', upstream_response_time)

    # $upstream_cache_status Did we hit or miss an nginx cache
    upstream_cache_status = line_parts[6]
    if upstream_cache_status == '-':
        upstream_cache_status = None
    if DEBUG:
        print('$upstream_cache_status:  ', upstream_cache_status)

    # $body_bytes_sent is the size of the finished response in bytes
    body_bytes_sent = int(line_parts[7])
    if DEBUG:
        print('$body_bytes_sent:        ', body_bytes_sent)

    # $scheme is the scheme (http or https) used in the request
    scheme = line_parts[9].strip('"').upper()
    if DEBUG:
        print('$scheme:                 ', scheme)

    # $request is the resource requested along with the verb and protocol, eg: `GET /index.html HTTP/1.0`
    request = ' '.join(line_parts[10:13])
    http_verb = line_parts[10].upper()
    request_path = line_parts[11]
    protocol = line_parts[12].strip('"')
    if DEBUG:
        print('$request:                ', request)
        print('http_verb:               ', http_verb)
        print('request_path:            ', request_path)
        print('protocol:                ', protocol)

    # $http_user_agent
    http_user_agent = ' '.join(line_parts[13:]).strip('"')
    if http_user_agent == '-':
        http_user_agent = None
    if DEBUG:
        print('$http_user_agent:        ', http_user_agent)

    return Request(
        msec,
        datetime,
        remote_addr,
        status,
        request_time,
        upstream_response_time,
        upstream_cache_status,
        body_bytes_sent,
        scheme,
        request,
        http_verb,
        request_path,
        protocol,
        http_user_agent,
    )
