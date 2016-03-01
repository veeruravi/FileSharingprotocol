#!/usr/bin/python           # This is client.py file

import socket
import sys
import random
import hashlib
               # Import socket module
EOF="EOF"
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 1234
port = raw_input("PORT:")
s.connect((host, int(port)))


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


def download_file_udp(s,command):
	s.send(command)
	file_exists = s.recv(1024)
	if file_exists=="no such file exist":
		print "no such file exist"
	else:
		udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		udp_port = s.recv(1024)
		s.send("recieved")
		addr = (host,int(udp_port))
		if s.recv(1024)=="ready":
			udp_socket.sendto("ready",addr)
			x=""
			f = open(command.split()[2],"wb")
			while x!=EOF:
				x,addr = udp_socket.recvfrom(1024)
				if x!=EOF:
					#print "recieved:",x
					f.write(x)
				udp_socket.sendto(str("recieved :"+x),addr)
			f.close()
			data,addr = udp_socket.recvfrom(1024)
			hash_of_recived_file = data.split("$")[1]
			print data.split("$")[0]+" "+hash_of_recived_file
			udp_socket.sendto("done",addr) 
			f = open(command.split()[2],'rb')
			hash_of_file = hashlib.md5(f.read()).hexdigest()
			f.close()
			if hash_of_recived_file==hash_of_file:
				print "sucessfully Downloaded : %s"%command.split()[2]
			else:
				print "Downloading Failed"
		


def download_file_tcp(s,input):
	s.send(input)
	x = s.recv(1024)
	if x=="no such file exist":
		print "no such file exist"
	else:
		f=open(input.split()[2],"wb")
		while x!=EOF:
			#print "recieved:	",x
			f.write(x)
			s.send("recieved:	%s"%(x))
			x = s.recv(1024)
		f.close()
		data = s.recv(1024)
		hash_of_recived_file = data.split("$")[1]
		print data.split("$")[0]+" "+hash_of_recived_file
		s.send("done")
		f = open(input.split()[2],'rb')
		hash_of_file = hashlib.md5(f.read()).hexdigest()
		f.close()
		if hash_of_file==hash_of_recived_file:
			print "sucessfully Downloaded: %s"%input.split()[2]
		else:
			print "Downloading Failed"


def shortlist(s,time1,time2):
	time11 = time1.split("/")
	s.send(str(time11[0]+" "+time11[1]))
	x = s.recv(1024)
	if x=="recieved":
		time22 = time2.split("/")
		s.send(str(time22[0]+" "+time22[1]))
		x1 = s.recv(1024)
		if x1=="recieved":
			s.send("hi")
			x2=""
			while x2!="EOF":
				x2 = s.recv(1024)
				if x2!="EOF":
					print x2
				s.send("recieved")
		else:
			print "failed to send! RETRY1"
	else:
		print "failed to send! RETRY2"


def longlist(s):
	x = ""
	while x!="EOF":
		x2 = s.recv(1024)
		s.send("recieved")
		if x2!="EOF":
			print x2
		else:
			break


def regex(s,reg):
	s.send(reg)
	if s.recv(1024)=="recieved":
		s.send("hi")
		x = ""
		i = 0
		while x!="EOF":
			x2 = s.recv(1024)
			s.send("recieved")
			i += 1
			if x2!="EOF":
				print x2
			else:
				break
		if i==1:
			print "		No such file with that regex"

def verify(s,filename):
	s.send(filename)
	file_exists = s.recv(1024)
	if file_exists=="no such file exist":
		print "no such file exist"
	else:
		s.send("hi")
		x=""
		while x!="EOF":
			x = s.recv(1024)
			if x!="EOF":
				s.send("recieved")
				print x
			else:
				break

	return


def checkall(s):
	filename=""
	while filename!="EOF":
		filename = s.recv(1024)
		if filename!="EOF":
			print filename
			s.send("recieved")
		elif filename=="ERROR":
			print "ERROR"
			return


def check_indexget(command):
	if command.find("shortlist")!=-1:
		command1 = command.split()
		if len(command1)==4:
			time1 = command1[2].split("/")
			time2 = command1[3].split("/")
			if len(time2)==2 and len(time1)==2:
				if len(time1[0].split("-"))==3 and len(time1[1].split(":"))==3 and len(time2[0].split("-"))==3 and len(time2[1].split(":"))==3:
					return True
				else:
					print "		ERROR:Enter a valid time"
			else:
				print "		ERROR:Enter a valid time"
		else:
			print "		ERROR:Invalid Input"
			return False
	else:
		return True


def client():
	print s.recv(1024)
	flag=0
	f = open(".history","a")
	while True:
		path = str("type what you want:")
		input1 = raw_input(path)
		f.write(str(input1+"\n"))
		if input1.find("FileDownload")!=-1:
			input2 = input1.split()
			if len(input2)==3:
				if input1.lower().find("tcp")!=-1:
					download_file_tcp(s,input1)
				elif input1.lower().find("udp")!=-1:
					download_file_udp(s,input1)
				else:
					print "		ERROR:Enter a flag either tcp or udp"
				flag=0
			else:
				if input1.lower().file("tcp")!=-1 or input1.lower().file("udp")!=-1:
					print "		ERROR:Enter a filename you want to download"
				else:
					print "		ERROR:Give the correct command"
		elif input1.find("IndexGet")!=-1:
			if check_indexget(input1)==True:
				s.send("IndexGet")
				if s.recv(1024)=="recieved":
					ls = input1.split()
					if strcmp(ls[1],"shortlist")==True:
						s.send("shortlist")
						if s.recv(1024)=="recieved":
							shortlist(s,ls[2],ls[3])
					elif strcmp(ls[1],"longlist")==True:	
						s.send("longlist")
						if s.recv(1024)=="recieved":
							longlist(s)
					else:
						s.send("regex")
						if s.recv(1024)=="recieved":
							regex(s,ls[1])
			flag=0
		elif input1.find("FileHash")!=-1:
			s.send("FileHash")
			if s.recv(1024)=="recieved":
				ls = input1.split()
				if strcmp(ls[1],"verify")==True:
					s.send("verify")
					if s.recv(1024)=="recieved":
						verify(s,ls[2])
						#print "verify"
				elif strcmp(ls[1],"checkall")==True:	
					s.send("checkall")
					if s.recv(1024)=="recieved":
						checkall(s)
						#print "checkall"
				else:
					s.send("no command found")
					print "Invalid command"
			flag=0
		elif input1=="quit":
			s.send("quit")
			flag=0
			break
		else:
			print "Invalid command"
			flag=1
		
		#elif input1.find("cd")!=-1:
		#	s.send(input1)
		#	print s.recv(1024)
		#	s.send("recieved")
		#print "longlist1"
	s.close()
	f.close()                    




client()