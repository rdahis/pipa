#!/usr/bin/env python2.7
import requests
import threading

req = requests.get( 'http://www.camara.gov.br/cotas/AnosAnteriores.zip', stream=True)


from subprocess import Popen, PIPE

ppp = Popen('funzip', stdin=PIPE, stdout=PIPE, shell=True)


class DownloadThread(threading.Thread):
	def run(self):
		try:
			for l in req.iter_content(1024*1024):
				ppp.stdin.write(l)
		except Exception as e:
			print e
		finally:
			ppp.stdin.close()

class ParsingThread(threading.Thread):
	def run(self):
		item = 0
		while True:
			piece = ppp.stdout.read(1024*1024)
			if not piece: break
			item +=1
			print item
			if item == 100000:
				req.close()


t1 = DownloadThread()
t2 = ParsingThread()
t1.start()
t2.start()
t1.join()
t2.join()


