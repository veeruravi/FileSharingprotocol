#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import os
import sys
import random
import hashlib

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name

def port(n):
	try:
		x = random.randint(1000,9999)
		n.bind((host,x))
		return x
	except socket.error, e:
		port(n)



port1 = port(s)
print port1
#s.bind((host, int(port1)))        # Bind to the port
s.listen(1)           

def strcmp(s1,s2):
	if len(s1)==len(s2):
		i = 0
		while i<len(s1):
			if s1[i]!=s2[i]:
				return False
			i+=1
		return True
	else:
		return False


def udpport(m):
	try:
		x = random.randint(1000,9999)
		m.bind((host,x))
		return x
	except socket.error, e:
		udpport(m)


def send_file_tcp(c,filename):
	f = open(filename,"rb")
	byte = f.read(1024)
	print "sending file",filename
	while byte:
		#print "sending		:",byte
		c.send(byte)
		c.recv(1024)
		byte = f.read(1024)
	c.send("EOF")
	f.close()
	f = open(filename,'rb')
	hash_of_file = hashlib.md5(f.read()).hexdigest()
	f.close()
	ls = os.popen("ls -l %s"%filename).read()
	ls1 = ls.split()
	size = ls1[len(ls1)-5]
	last_modified_time = os.popen("stat -c %%y %s"%filename).read()
	c.send(filename+" "+size+"bytes "+last_modified_time+"$"+hash_of_file)
	if c.recv(1024)=="done":
		return


def send_file_udp(c,filename):
	udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	udp_port= udpport(udp_socket)
	#udp_socket.bind((host,udp_port))
	c.send(str(udp_port))
	addr = (host,udp_port)
	if c.recv(1024)=="recieved":
		c.send("ready")
		x,addr = udp_socket.recvfrom(1024)
		print x
		f = open(filename,"rb")
		byte = f.read(1024)
		print "sending file :",filename
		while byte:
			#print "sending : ",byte
			udp_socket.sendto(byte,addr)
			x,addr = udp_socket.recvfrom(1024)
			#print x
			byte = f.read(1024)
		udp_socket.sendto("EOF",addr)
		f.close()
		f = open(filename,'rb')
		hash_of_file = hashlib.md5(f.read()).hexdigest()
		f.close()
		ls = os.popen("ls -l %s"%filename).read()
		ls1 = ls.split()
		size = ls1[len(ls1)-5]
		last_modified_time = os.popen("stat -c %%y %s"%filename).read()
		udp_socket.sendto(filename+" "+size+"bytes "+last_modified_time+"$"+hash_of_file,addr)
		if udp_socket.recvfrom(1024)=="done":
			return
		
		


def send_ls(s,command):
	x=""
	while x!="recieved":
		#print "in while"
		ls = os.popen(command).read()
		s.send(ls)
		x=s.recv(1024)
		print x
		if x=="recieved":
			break
	#print x,"2"


def check_file_exists(filename):
	print filename
	l = os.popen("find %s"%filename).read()
	l1 = l.split("\n")
	# if len(l1)>1:
	# 	return False
	return strcmp(l1[0],filename)
	# x = l.split("\n")
	# for k in x:
	# 	y = k.split(" ")
	# 	if strcmp(y[len(y)-1],filename)==True:
	# 		return True
	# return False

def check_directory_exists(directory):
	l = os.popen("ls -l").read()
	x = l.split("\n")
	for k in x:
		y = k.split(" ")
		for k1 in y:
			if strcmp(k1,directory)==True:
				if "d" in y[0]:
					return True
	return False


def shortlist(c):
	time1 = c.recv(1024)
	print "time1 %s"%time1
	c.send("recieved")
	time2 = c.recv(1024)
	print "time2 %s"%time2
	c.send("recieved")
	x = c.recv(1024)
	if x=="hi":
		l1 = os.popen("find %s -newermt %s ! -newermt  %s -not -path '*/\.*' -type f"%(".",str('"'+time1+'"'),str('"'+time2+'"'))).read()
		l2 = l1.split("\n")
		for k in l2:
			if strcmp(k,".")==False:
				print "sending %s"%k
				l = os.popen("ls -l %s"%(k)).read()
				l3 = l.split("\n")
				l4 = os.popen("file %s"%k).read()
				l5 = l4.split(":")
				l6=""
				if len(l5)>1:
					l6 = str(l5[1])
				if "total" not in l3[0]:
					l7 = l.split()
					le = len(l7)
					c.send(str(l7[le-1]+"\n     size:"+l7[le-5]+" bytes\n     time: "+l7[le-4]+" "+l7[le-3]+" "+l7[le-2]+"\n     type:"+l6))
					#print l
					x1 = c.recv(1024)
					if x1=="recieved":
						pass
		c.send("EOF")
		x1 =c.recv(1024)
		if x1=="recieved":
			return


def longlist(c):
	l1 = os.popen("find . -not -path '*/\.*' -type f").read()
	l2 = l1.split("\n")
	for k in l2:
		if strcmp(k,".")==False:
			print "sending %s"%k
			l = os.popen("ls -l %s"%(k)).read()
			l3 = l.split("\n")
			l4 = os.popen("file %s"%k).read()
			l5 = l4.split(":")
			l6=""
			if len(l5)>1:
				l6 = str(l5[1])
			if "total" not in l3[0]:
				l7 = l.split()
				le = len(l7)
				c.send(str(l7[le-1]+"\n     size:"+l7[le-5]+" bytes\n     time: "+l7[le-4]+" "+l7[le-3]+" "+l7[le-2]+"\n     type:"+l6))
				#print l
				x1 = c.recv(1024)
				if x1=="recieved":
					pass
	c.send("EOF")
	x1 =c.recv(1024)
	if x1=="recieved":
		return


def regex(c):
	reg = c.recv(1024)
	c.send("recieved")
	if c.recv(1024)=="hi":
		l = os.popen("find ./ -regextype sed -regex %s"%(reg)).read()
		l2 = l.split("\n")
		for k in l2:
			if strcmp(k,".")==False and k!="":
				print "sending %s"%k
				l = os.popen("ls -l %s"%(k)).read()
				l3 = l.split("\n")
				l4 = os.popen("file %s"%k).read()
				l5 = l4.split(":")
				l6=""
				if len(l5)>1:
					l6 = str(l5[1])
				if "total" not in l3[0]:
					l7 = l.split()
					le = len(l7)
					c.send(str(l7[le-1]+"\n     size:"+l7[le-5]+" bytes\n     time: "+l7[le-4]+" "+l7[le-3]+" "+l7[le-2]+"\n     type:"+l6))
					#print l
					x1 = c.recv(1024)
					if x1=="recieved":
						pass
				# print "sending %s"%x
				# c.send(x)
				# if c.recv(1024)=="recieved":
				# 	pass
		c.send("EOF")
		if c.recv(1024)=="recieved":
			return


def verify(c):
	filename = c.recv(1024)
	file_exist = check_file_exists(filename)
	if file_exist==True:
		c.send("recieved")
		if c.recv(1024)=="hi":
			checksum = os.popen("cksum %s"%filename).read()
			last_modified_time = os.popen("stat -c %%y %s"%filename).read()
			print checksum,last_modified_time
			checksum1 = checksum.split()
			c.send(checksum1[2]+"\n     checksum="+checksum1[0])
			print c.recv(1024)
			c.send("     last modified time :"+last_modified_time)
			print c.recv(1024)
			c.send("EOF")
			return
	else:
		c.send("no such file exist")
				

def checkall(c):
	files = os.popen("find . -not -path '*/\.*' -type f").read()
	files1 = files.split("\n")
	i = 0
	while i<len(files1) and files1[i]!="":
		filename =files1[i]
		checksum = os.popen("cksum %s"%filename).read()
		last_modified_time = os.popen("stat -c %%y %s"%filename).read()
		checksum1 = checksum.split()
		c.send(checksum1[2]+"\n     checksum ="+checksum1[0]+"\n     last modified time: "+last_modified_time)
	#	print filename
		if c.recv(1024)=="recieved":
			pass
		else:
			c.send("ERROR")
			print "ERROR"
			return
		i+=1
	c.send("EOF")


def server():      # Now wait for client connection.
	loop = True
	while loop:
		c, addr = s.accept()     # Establish connection with client.
		print 'Got connection from', addr
		c.send('Thank youfor connecting')
		while True:
			#c.send(os.popen("pwd").read())
			print "waiting for response:	"
			asked = c.recv(1024)
			print "$"+asked+"$"
			if asked.find("FileDownload")!=-1:
				f = asked.split()
				file_exist = check_file_exists(f[2])
				print file_exist
				if file_exist==True:
					if asked.lower().find("tcp")!=-1:
						send_file_tcp(c,f[2])
					elif asked.lower().find("udp")!=-1:
						c.send("exist")
						send_file_udp(c,f[2])
				else:
					c.send("no such file exist")
			elif asked.find("IndexGet")!=-1:
				c.send("recieved")
				input1 = c.recv(1024)
				c.send("recieved")
				if input1=="shortlist":
					shortlist(c)
					print "shortlist"
				elif input1=="longlist":
					longlist(c)
					print "longlist"
				else:
					regex(c)
					print "regex"
			elif asked.find("FileHash")!=-1:
				c.send("recieved")
				input1 = c.recv(1024)
				if strcmp(input1,"no command found")==False:
					c.send("recieved")
					if input1=="verify":
						print "verify"
						verify(c)
					elif input1=="checkall":
						checkall(c)
						print "checkall"
			elif asked.find("cd")!=-1:
				if check_directory_exists(asked.split()[1]) == True:
					change_directory()
					c.send("True")
				else:
					c.send("False")
			elif asked=="quit":
				loop = False
				c.close()
				break
		c.close()                # Close the connection


server()