import threading, time, requests, os, sys, json, datetime
from Similarity import Similarity

class PagesChecker(object):
	"""docstring for PagesChecker."""

	def __init__(self, urls, onchange=None):#onchange is a function with onchange(url)

		########################################################################
		#HYPERPARAMETERS
		self.datapath = "./data"
		self.periode = 10*60 #check every hour
		self.deltastart = 3 #start thread with a delta time of 3 sec
		self.max_change_ratio = 0.10
		########################################################################

		super(PagesChecker, self).__init__()
		self.isrunning = False
		self.urls = urls
		self.onchange = onchange
		self.threads = []
		self.sm = Similarity()

		if not os.path.exists(self.datapath) or os.path.exists(self.datapath) and not os.path.isdir(self.datapath):
			os.mkdir(self.datapath, 0o755)

	def run(self):
		self.isrunning = True
		urls = self.urls
		self.urls = []
		for url in urls:
			self.addNewChecker(url)
			time.sleep(self.deltastart)

	def stop(self):
		self.isrunning = False
		for thread in self.threads:
			thread.stop()

	def state(self):
		print("Got "+str(len(self.threads))+" running !")

	def getFileNameFromUrl(self, url):
		nurl = url.replace("https://", "").replace("http://", "").replace("/", "-").replace(".html", "").replace(".php", "").replace(".js", "").replace(".", "_")
		return self.datapath+"/"+nurl

	def formatDate(self):
		return '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

	def saveState(self, url, data):
		f = open(self.getFileNameFromUrl(url), "w+")
		f.truncate(0)
		f.seek(0)
		f.write(json.dumps(data))
		f.close()

	def strIsSame(self, html1, html2):
		if len(html1) == len(html2):
			return self.sm.isSimilar(html1, html2)
		else:
			return False

	def addNewChecker(self, url):
		if not os.path.exists(self.getFileNameFromUrl(url)):
			f = open(self.getFileNameFromUrl(url), "w+")
			f.write(json.dumps({"url":url, "created_at":self.formatDate(), "html":"", "last_check":"0", "nb_change":0}))
			f.close()
		t = threading.Thread(target=self.worker, args=(url,))
		self.threads.append(t)
		self.urls.append(url)
		t.start()

	def stopChecker(self, url):
		for i in range(0, len(self.urls)):
			if self.urls[i] == url:
				self.threads[i].stop()
				self.threads.pop(i)
				self.urls.pop(i)
				break

	def worker(self, url):
		html = str(requests.get(url).content, "utf-8")

		datafile = open(self.getFileNameFromUrl(url), "r+")
		raw = datafile.read()
		data = json.loads(raw)
		datafile.close()

		#isSame = self.strIsSame(html, data["html"])
		distance = sum([1 for x, y in zip(html, data["html"]) if x.lower() != y.lower()])
		change_ratio = distance*2/(len(html)+len(data["html"]))

		if(change_ratio > self.max_change_ratio or data["html"] == ""):
			data["nb_change"] += 1
			data["html"] = html

			self.onchange(url)

		data["last_check"] = self.formatDate()
		self.saveState(url, data)
		time.sleep(self.periode)

if __name__ == '__main__':

	def onPageChangeEvent(url):
		print("onPageChangeEvent("+str(url)+")")


	#call onPageChangeEvent each time a webpage has changed
	urls = ["https://tiptap.pro", "https://www.lemonde.fr", "https://appcom.xyz"]

	pc = PagesChecker(urls, onchange=onPageChangeEvent)
	pc.run()
