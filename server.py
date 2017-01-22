#  coding: utf-8 
import SocketServer, os.path, mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

	header = "" #send it to the browser or curler

	def sendPage(self, path):
			#http://stackoverflow.com/questions/34307339/reading-a-txt-file-from-a-folder-in-python-script
########cite this better later
		print "i will send a page"
#how to use mimetypes http://stackoverflow.com/questions/947372/custom-simple-python-http-server-not-serving-css-files
		mimetype, _ = mimetypes.guess_type(os.path.normpath(os.curdir + path))
		ctype = 'Content-Type: ' + mimetype + ';\r\n' 
		print "path: %s" % path[1:]
		#csize = '\nContent-Length ' + str(os.path.getsize(path[1:])) ###copied function call idea from ryans code

		

		f = open( os.path.normpath(os.curdir + path), 'r')
		contents = f.read()
		f.close()
		self.header = "HTTP/1.1 200 OK\r\n"
		csize = 'Content-Length: ' + str(len(contents.encode('utf-8'))) + '\r\n'
		self.request.sendall(self.header + ctype + csize + '\r\n' + contents) 

    
	def handle(self):
		self.data = self.request.recv(1024).strip()
		command = self.data.split()
		print "your command was %s" % command[0]
		#print "you wanted %s" % command[1]
		#print ("Got a request of: %s\n" % self.data)
		if command[0] != "GET":
			#not implemented, send error code in header
			self.header = "HTTP/1.1 405 Method Not Allowed\r\n"
			self.request.sendall(self.header) 
		
		else:
			#get the files from www/
			path = "/www"
			path = path + command[1] #get the location specified
			
			#print "path: %s " % os.path.normpath(os.curdir + path)
			print "path: %s " % os.curdir + path

			#for the 'how secure are you?' test
			#first check if the end of the path has a /
			valid = False			
			if( path[-1] == '/'):
				valid = True

			#then normalize the path
			path = os.path.normpath(path)
			#then proceed like usual
			if(valid == True):
				path = path + '/'


			if(os.path.isdir( os.curdir + path) ): #check if this path is a directory
				
				#if theres no slash at the end, perform a redirect
				if( path[-1] != '/'):	

					relocation = path.split('/')			
					print "redirecting"
					print "R: path: %s" % path
					self.header = "HTTP/1.1 302 Found\r\n"
					#learned that I only need to send the latter part of the path from looking at Ryan's code. otherwise the redirect is the incorrect URL
					self.request.sendall(self.header + "Location: " + path[4:] + '/' + '\r\n');
				#otherwise, send the appropriate index.html
				else:
					print "ok directory"
					path = path + "index.html"
					self.sendPage(path)

				
			else:
				
				if(os.path.isfile( os.curdir + path) ): #check if this path is a file
					print "itsa file!"

					self.sendPage(path) #how to call this function http://stackoverflow.com/questions/24291941/python-nameerror-global-name-sortlist-is-not-defined-during-recursion

				#print ("the request was %s\n" % self.data)
				else: #the current path is not a file nor directory
					print "not a file or directory"
					self.header = "HTTP/1.1 404 Page Not Found\r\n"
					ptype = 'Content-Type: text/html;\r\n'
					
					page = '<!DOCTYPE html><html><head>Error 404 Page Not Found</head></html>'
					psize = 'Content-Length: ' + str(len(page.encode('utf-8'))) + '\r\n'
					self.request.sendall(self.header + ptype + psize + '\r\n' + page) 

#			self.request.sendall("OK")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
