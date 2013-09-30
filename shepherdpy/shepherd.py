#!/usr/bin/env python

"""A companion library for mincemeatpy for management of servers and clients."""


################################################################################
# Copyright (c) 2013 Joshua Petitt
# https://github.com/jpmec/shepherdpy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

# pylint: disable=W0403
# pylint: disable=W0201

import collections
import logging
import optparse
import socket
import sys
import time
from multiprocessing import Pool, Process
import mincemeat

VERSION = "0.0.2"

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PASSWORD = ''
DEFAULT_PORT = mincemeat.DEFAULT_PORT

MINIMUM_CLIENT_SLEEP_SECONDS = 1




# pylint: disable=R0904
class Client(mincemeat.Client):
    """The client"""

    def __init__(self):
        mincemeat.Client.__init__(self)

    def handle_error(self):
        raise

    def run(self, options):
        """Run the client with the given options"""

        client_sleep_seconds = None
        if (options.client_sleep_seconds is not None):
            client_sleep_seconds = float(options.client_sleep_seconds)

        while True:
            try:
                self.password = options.password
                self.conn(options.hostname, options.port)
                break

            except socket.error:
                exc_info = sys.exc_info()
                logging.debug("%s:{hostname=%s, port=%s}:%s",
                    exc_info[0],
                    options.hostname,
                    options.port,
                    exc_info[1])

                if (client_sleep_seconds is None):
                    time.sleep(MINIMUM_CLIENT_SLEEP_SECONDS)
                    break
                else:
                    time.sleep(client_sleep_seconds)

                self.__init__()

            except KeyboardInterrupt:
                return

            except:
                exc_info = sys.exc_info()
                logging.exception("%s:%s", exc_info[0], exc_info[1])
                break

    @staticmethod
    def options_parser():
        """Returns options parser for Client"""

        parser = optparse.OptionParser(
            usage='%prog [options]',
            version='%%prog %s'%VERSION)
        parser.add_option('-p', '--password', dest='password',
            default=DEFAULT_PASSWORD, help='password')
        parser.add_option('-H', '--hostname', dest='hostname',
            default=DEFAULT_HOSTNAME, help='hostname')
        parser.add_option('-P', '--port', dest='port', type='int',
            default=DEFAULT_PORT, help='port')
        parser.add_option('-v', '--verbose', dest='verbose',
            action='store_true')
        parser.add_option('-V', '--loud', dest='loud', action='store_true')
        parser.add_option('-q', '--quiet', dest='quiet', action='store_true')
        parser.add_option('-n', '--number_of_clients', dest='number_of_clients',
            default='1', help='number of client processes')
        parser.add_option('-s', '--sleep', dest='client_sleep_seconds',
            default=None, help='client sleep seconds')
        parser.add_option('-t', '--client_timeout',
            dest='client_timeout_seconds',
            default=None, help='worker timeout seconds')
        parser.add_option('-8', '--run_forever', dest='run_forever',
            action='store_true')
        parser.add_option('-i', '--input_filename', dest='input_filename',
            default='', help='input filename')

        return parser




# pylint: disable=R0904
class Server(mincemeat.Server):
    """The server"""

    def __init__(self, datasource=None):
        mincemeat.Server.__init__(self)
        self.datasource = datasource
        self.mapfn = map_default
        self.reducefn = reduce_default

    @staticmethod
    def options_parser():
        """Returns an options parser for Server"""

        parser = optparse.OptionParser(
            usage='%prog [options]',
            version='%%prog %s'%VERSION)
        parser.add_option('-p', '--password', dest='password',
            default=DEFAULT_PASSWORD, help='password')
        parser.add_option('-P', '--port', dest='port', type='int',
            default=DEFAULT_PORT, help='port')
        parser.add_option('-v', '--verbose', dest='verbose',
            action='store_true')
        parser.add_option('-V', '--loud', dest='loud',
            action='store_true')
        parser.add_option('-q', '--quiet', dest='quiet',
            action='store_true')

        return parser



def run_client(options):
    """Global method to run a client with the given options"""

    run_forever = True
    while run_forever:
        try:
            client = Client()
            client.run(options)

        except KeyboardInterrupt:
            break

        except:
            exc_info = sys.exc_info()
            logging.exception("%s:%s", exc_info[0], exc_info[1])
            break

        finally:
            if not 'run_forever' in options:
                run_forever = False




def run_clients(options=None):
    """Global method to run a pool of clients"""

    parser = Client.options_parser()
    (default_options, _) = parser.parse_args([])

    if (options is not None):
        try:
            default_options.__dict__.update(options.__dict__)
        except AttributeError:
            default_options.__dict__.update(options)

    options = default_options

    number_of_clients = int(options.number_of_clients)

    pool = Pool(processes=number_of_clients)

    try:
        for _ in range(number_of_clients):
            pool.apply_async(run_client, [options])

    except KeyboardInterrupt:
        exc_info = sys.exc_info()
        logging.debug("%s:%s", exc_info[0], exc_info[1])
        pool.terminate()
        pool.join()

    except:
        exc_info = sys.exc_info()
        logging.exception("%s:%s", exc_info[0], exc_info[1])
        pool.terminate()

    else:
        pool.close()

    finally:
        pool.join()









def run_server(options):
    """Global method to run a Server"""

    parser = Client.options_parser()
    (default_options, _) = parser.parse_args([])

    if (options is not None):
        try:
            default_options.__dict__.update(options.__dict__)
        except AttributeError:
            default_options.__dict__.update(options)

    options = default_options

    logging.debug(options)

    datasource = None
    if (isinstance(options.datasource, collections.Mapping)):
        datasource = options.datasource
    else:
        datasource = dict(enumerate(options.datasource))

    server = None
    if ('server' in options.__dict__):
        server = options.server(datasource)
    else:
        server = Server(datasource)


    if ('mapfn' in options.__dict__):
        server.mapfn = options.mapfn

    if ('reducefn' in options.__dict__):
        server.reducefn = options.reducefn

    return server.run_server(password=options.password)




def run(**kwargs):
    """Global method to run a server and a pool of clients"""

    server_pool = Pool(processes=1)
    server_process = server_pool.apply_async(run_server, [kwargs])
    run_clients()
    return server_process.get()




def map_count(_, value):
    """Generate count for each split value"""
    for word in value.split():
        yield word, 1


def reduce_count(_, values):
    """Sum values"""
    return sum(values)


def map_default(key, values):
    """Default map, will return key and values unmodified"""

    yield key, values


def reduce_default(_, values):
    """Default reduce, will return values unmodified"""

    if (len(values) == 1):
        return values[0]
    else:
        return values




class WordCountServer(Server):
    """A server for simple word counting"""

    def __init__(self, datasource=None):
        Server.__init__(self, datasource)
        self.mapfn = map_count
        self.reducefn = reduce_count




def main():
    """Main method, called by default"""

    parser = Client.options_parser()
    (options, args) = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.INFO)
    if options.loud:
        logging.basicConfig(level=logging.DEBUG)
    if options.quiet:
        logging.basicConfig(level=logging.FATAL)

    if len(args) > 0:
        options.hostname = args[0]

    logging.debug('options: %s', options)


    clients_process = Process(target=run_clients, args=(options,))
    clients_process.start()
    clients_process.join()




if __name__ == '__main__':
    main()
