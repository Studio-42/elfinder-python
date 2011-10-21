#!/usr/bin/env python

import cgi
## CGI debug
# import cgitb
# cgitb.enable()
try:
	import json
except ImportError:
	import simplejson as json
import elFinder

# configure connector options
opts = {
	## required options
	# 'root': '/path/to/files', # full path to your files
	# 'URL': 'http://mydomain.tld/path/to/files' # can be absolute or relative
	'root': '.',
	'URL': '.',
	## other options
	'debug': True,
	# 'fileURL': False,  # download files using connector, no direct urls to files
	# 'dirSize': True,
	# 'dotFiles': True,
	# 'perms': {
	# 	'backup': {
	# 		'read': True,
	# 		'write': False,
	# 		'rm': False
	# 	},
	# 	'^/pics': {
	# 		'read': True,
	# 		'write': False,
	# 		'rm': False
	# 	}
	# },
	# 'uploadDeny': ['image', 'application'],
	# 'uploadAllow': ['image/png', 'image/jpeg'],
	# 'uploadOrder': ['deny', 'allow'],
	# 'disabled': ['rename', 'quicklook', 'upload'],
	# 'disabled': ['archive', 'extract'], # this will also disable archivers check
}


# init connector and pass options
elf = elFinder.connector(opts)

# fetch only needed GET/POST parameters
httpRequest = {}
form = cgi.FieldStorage()
for field in elf.httpAllowedParameters:
	if field in form:
		httpRequest[field] = form.getvalue(field)

		# Django hack by Kidwind
		if field == 'targets[]' and hasattr(form, 'getlist'):
			httpRequest[field] = form.getlist(field)

		# handle CGI upload
		if field == 'upload[]':
			upFiles = {}
			cgiUploadFiles = form[field]
			if not isinstance(cgiUploadFiles, list):
				cgiUploadFiles = [cgiUploadFiles]
			for up in cgiUploadFiles:
				if up.filename:
					upFiles[up.filename] = up.file # pack dict(filename: filedescriptor)
			httpRequest[field] = upFiles


# run connector with parameters
status, header, response = elf.run(httpRequest)

# get connector output and print it out

# code below is tested with apache only (maybe other server need other method?)
if status == 200:
	print 'Status: 200'
elif status == 403:
	print 'Status: 403'
elif status == 404:
	print 'Status: 404'

if len(header) >= 1:
	for h, v in header.iteritems():
		print h + ': ' + v
	print

if not response is None and status == 200:
	# send file
	if 'file' in response and isinstance(response['file'], file):
		print response['file'].read()
		response['file'].close()
	# output json
	else:
		print json.dumps(response, indent = True)

## logging
#import sys
#log = open('/home/troex/Sites/git/elfinder-2.x/files/out.log', 'w')
#print >>log, 'cuf: ', cgiUploadFiles
#log.close()

## another aproach
## get connector output and print it out
#if elf.httpStatusCode == 200:
#	print 'HTTP/1.1 200 OK'
#elif elf.httpStatusCode == 403:
#	print 'HTTP/1.x 403 Access Denied'
#elif elf.httpStatusCode == 404:
#	print 'HTTP/1.x 404 Not Found'
#
#if len(elf.httpHeader) >= 1:
#	for header, value in elf.httpHeader.iteritems():
#		print header + ': ' + value
#	print
#
#if not elf.httpResponse is None:
#	if isinstance(elf.httpResponse['file'], file):
#		print elf.httpResponse['file'].read()
#		elf.httpResponse['file'].close()
#	else:
#		print json.dumps(elf.httpResponse, indent = True)
#
