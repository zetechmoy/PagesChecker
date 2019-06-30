from pageschecker import PagesChecker

def onPageChangeEvent(url):
	print("onPageChangeEvent("+str(url)+")")


#call onPageChangeEvent each time a webpage has changed
urls = ["https://tiptap.pro", "https://www.lemonde.fr", "https://appcom.xyz"]

pc = PagesChecker(urls, onchange=onPageChangeEvent)
pc.run()
