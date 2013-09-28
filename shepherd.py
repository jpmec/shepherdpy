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
import socket
import sys


VERSION = "0.0.1"

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PASSWORD = ''
DEFAULT_PORT = mincemeat.DEFAULT_PORT




class Client(mincemeat.Client):

	def __init__(self):
		mincemeat.Client.__init__(self)

	def handle_error(self):
		raise




def run_client(options = {}):
	try:
		client = Client()
		client.password = options.password
		client.conn(options.hostname, options.port)
	except socket.error:
		exc_info = sys.exc_info()
		logging.critical("%s:{hostname=%s, port=%s}:%s",
			exc_info[0],
			options.hostname,
			options.port,
			exc_info[1])
	except:
		exc_info = sys.exc_info()
		logging.exception("%s:%s", exc_info[0], exc_info[1])





if __name__ == '__main__':

	parser = optparse.OptionParser(usage='%prog [options]', version='%%prog %s'%VERSION)
	parser.add_option('-p', '--password', dest='password', default=DEFAULT_PASSWORD, help='password')
	parser.add_option('-H', '--hostname', dest='hostname', default=DEFAULT_HOSTNAME, help='hostname')
	parser.add_option('-P', '--port', dest='port', type='int', default=DEFAULT_PORT, help='port')
	parser.add_option('-v', '--verbose', dest='verbose', action='store_true')
	parser.add_option('-V', '--loud', dest='loud', action='store_true')

	(options, args) = parser.parse_args()

	if options.verbose:
		logging.basicConfig(level=logging.INFO)
	if options.loud:
		logging.basicConfig(level=logging.DEBUG)

	if len(args) > 0:
		options.hostname = args[0]

	logging.debug('options: %s', options)

	run_client(options)
