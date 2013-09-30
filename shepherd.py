#!/usr/bin/env python

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

import collections
import logging
import mincemeat
import optparse
import socket
import sys
import time
from multiprocessing import Pool, Process


VERSION = "0.0.1"

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PASSWORD = ''
DEFAULT_PORT = mincemeat.DEFAULT_PORT

MINIMUM_CLIENT_SLEEP_SECONDS = 1




class Client(mincemeat.Client):

	def __init__(self):
		mincemeat.Client.__init__(self)

	def handle_error(self):
		raise

	def run(self, options):

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




class Server(mincemeat.Server):

	def __init__(self, datasource=None):
		mincemeat.Server.__init__(self)
		self.datasource = datasource
		self.mapfn = map_default
		self.reducefn = reduce_default




def run_client(options = {}):

	while True:
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
			if not options.run_forever:
				break




def client_options_parser():
	parser = optparse.OptionParser(usage='%prog [options]', version='%%prog %s'%VERSION)
	parser.add_option('-p', '--password', dest='password', default=DEFAULT_PASSWORD, help='password')
	parser.add_option('-H', '--hostname', dest='hostname', default=DEFAULT_HOSTNAME, help='hostname')
	parser.add_option('-P', '--port', dest='port', type='int', default=DEFAULT_PORT, help='port')
	parser.add_option('-v', '--verbose', dest='verbose', action='store_true')
	parser.add_option('-V', '--loud', dest='loud', action='store_true')
	parser.add_option('-q', '--quiet', dest='quiet', action='store_true')
	parser.add_option('-n', '--number_of_clients', dest='number_of_clients', default='1', help='number of client processes')
	parser.add_option('-s', '--sleep', dest='client_sleep_seconds', default=None, help='client sleep seconds')
	parser.add_option('-t', '--client_timeout', dest='client_timeout_seconds', default=None, help='worker timeout seconds')
	parser.add_option('-8', '--run_forever', dest='run_forever', action='store_true')
	parser.add_option('-i', '--input_filename', dest='input_filename', default='', help='input filename')

	return parser




def run_clients(options=None):

	parser = client_options_parser()
	(default_options, args) = parser.parse_args([])

	if (options is not None):
		try:
			default_options.__dict__.update(options.__dict__)
		except:
			default_options.__dict__.update(options)

	options = default_options

	number_of_clients = int(options.number_of_clients)

	pool = Pool(processes=number_of_clients)

	try:
		for i in range(number_of_clients):
			result = pool.apply_async(run_client, [options])

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




def server_options_parser():
	parser = optparse.OptionParser(usage='%prog [options]', version='%%prog %s'%VERSION)
	parser.add_option('-p', '--password', dest='password', default=DEFAULT_PASSWORD, help='password')
	parser.add_option('-P', '--port', dest='port', type='int', default=DEFAULT_PORT, help='port')
	parser.add_option('-v', '--verbose', dest='verbose', action='store_true')
	parser.add_option('-V', '--loud', dest='loud', action='store_true')
	parser.add_option('-q', '--quiet', dest='quiet', action='store_true')

	return parser




def run_server(options):

	parser = client_options_parser()
	(default_options, args) = parser.parse_args([])

	if (options is not None):
		try:
			default_options.__dict__.update(options.__dict__)
		except:
			default_options.__dict__.update(options)

	options = default_options

	logging.debug(options)

	datasource = None
	if (isinstance(options.datasource,collections.Mapping)):
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
	server_pool = Pool(processes=1)
	server_process = server_pool.apply_async(run_server, [kwargs])
	run_clients()
	return server_process.get()




def map_word_count(k, v):
    for w in v.split():
        yield w, 1


def reduce_word_count(k, vs):
    return sum(vs)


def map_default(k, v):
	yield k, v


def reduce_default(k, vs):
	if (len(vs) == 1):
		return vs[0]
	else:
		return vs




class WordCountServer(Server):

	def __init__(self, datasource=None):
		Server.__init__(self, datasource)
		self.mapfn = map_word_count
		self.reducefn = reduce_word_count




if __name__ == '__main__':

	parser = client_options_parser()
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


	p = Process(target=run_clients, args=(options,))
	p.start()
	p.join()
