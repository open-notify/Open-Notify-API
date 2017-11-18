#!./env/bin/python
import sys
import nginx_parse


# Change this to True to use the Mock_statsd in place of datadog
DEBUG = False


class Stats(object):
    """Stats class will take a raw line of log file input, read it, then report
    statistics about it.

    Initialize with a `statsd` interface and then call `listen` with a line of
    log file to be parsed.
    """

    def __init__(self, statsd):
        self.statsd = statsd

    def listen(self, line):

        # Use the nginx_parse library to unwrap a line of text
        # If we fail, log the problem line and give up
        try:
            request = nginx_parse.parseline(line)
        except:
            print("Failed to parse line {}".format(line))
            return

        # Note that we got a request
        statsd.increment('nginx.net.requests')

        # Count up HTTP response code numbers
        # Success! 100, 200, 202, 302, etc. All good.
        if request.status < 400:
            statsd.increment('nginx.net.2xx_status', tags=["endpoint:{}".format(request.endpoint_tag)])
        # Oh no! Bad requests
        if request.status >= 400 and request.status < 500:
            statsd.increment('nginx.net.4xx_status')
        # Probably good if we know about excessive 404s
        if request.status == 404:
            statsd.increment('nginx.net.404_status')
        # This is the client hanging up before we finish the request. Usually a sign of server overload
        if request.status == 499:
            statsd.increment('nginx.net.499_status')
        # Backend is probably down
        if request.status >= 500:
            statsd.increment('nginx.net.5xx_status')

        # Use `histogram` to count up average/median/min/man of request_times, divided by endpoint
        statsd.histogram('nginx.api.response_time', request.request_time, tags=["endpoint:{}".format(request.endpoint_tag)])

        # Use `histogram` to count up average/median/min/man of upstream_response_time, divided by endpoint
        if request.upstream_response_time is not None:
            statsd.histogram('nginx.api.upstream_time', request.upstream_response_time, tags=["endpoint:{}".format(request.endpoint_tag)])


class Mock_statsd(object):
    """A mock test class for `datadog.statsd` that has the same function
    signatures so it can be used for testing without hitting pushing stats to
    production. Used when DEBUG = True.

    To see if you got the right numbers and tags set, try printing the contents
    of `self.i` and `self.h` after sending some data to it.
    """

    def __init__(self):
        self.i = {}
        self.h = {}

    def increment(self, s, tags=None):
        if tags is not None:
            s = s + '_' + ''.join(tags)
        if s not in self.i:
            self.i[s] = 1
        else:
            self.i[s] = self.i[s] + 1

    def histogram(self, s, time, tags=None):
        if tags is not None:
            s = s + '_' + ''.join(tags)
        if s not in self.h:
            self.h[s] = [time]
        else:
            self.h[s].append(time)


if __name__ == '__main__':

    # `statsd` is either a mock object OR a datadog instance
    if DEBUG is True:
        statsd = Mock_statsd()
    else:
        from datadog import statsd

    # Loop forever (or until we stop feeding stdin)
    # Call this script like this:
    #   $ tail -F /var/log/file.log | datadog-monitor.py
    # to run forever and monitor a log
    stats = Stats(statsd)
    for line in sys.stdin:
        stats.listen(line)

    # If we're in debug we printout the results of our testrun
    if DEBUG is True:
        print("Recovered stats:")
        for i in statsd.i:
            print(i, ':', statsd.i[i])
        for h in statsd.h:
            print(h, ':', statsd.h[h])
