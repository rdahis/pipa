#!/usr/bin/env python2.7
import requests
import threading

req = requests.get( 'http://www.camara.gov.br/cotas/AnoAnterior.zip', stream=True)


from subprocess import Popen, PIPE

ppp = Popen('funzip', stdin=PIPE, stdout=PIPE, shell=True)


class DownloadThread(threading.Thread):
	def run(self):
		try:
			for l in req.iter_content():
				ppp.stdin.write(l)
		finally:
			ppp.stdin.close()

class ParsingThread(threading.Thread):
	def run(self):
		item = 0
		while True:
			piece = ppp.stdout.read(1024)
			if not piece: break
			print piece,
			item +=1
			if item == 1000:
				req.close()


t1 = DownloadThread()
t2 = ParsingThread()
t1.start()
t2.start()
t1.join()
t2.join()


