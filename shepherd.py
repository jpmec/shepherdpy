#!/usr/bin/env python

################################################################################
# Copyright (c) 2013 Joshua Petitt
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

import logging
import mincemeat
import optparse
#import signal
import socket
import sys
import time
from multiprocessing import Pool


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




def run_clients(options):

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


if __name__ == '__main__':

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
	parser.add_option("-8", "--run_forever", dest="run_forever", action="store_true")


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

	run_clients(options)
