#
#	knots.py
#	Scrape animatedknots.com/knotlist.php and make a hierarchy of knots.
#

__author__ = "Ray Dodds"

from bs4 import BeautifulSoup
import requests
import random as r

#	Global Constants
baseURL = "http://www.animatedknots.com/"
knotListURL = "knotlist.php"


def main():
	
	# Get the knot list page
	try:
		listPage = requests.get(baseURL+knotListURL)
	except ConnectionError as e:
		print(e)
	
	# Make sure that the page came back right
	if(listPage.status_code == 200):
		lpsoup = BeautifulSoup(listPage.content, 'html.parser')
	else:
		print("Error: Got status code", str(listPage.status_code))
		exit()

	# Get all links that are not styled and go somewhere
	aList = lpsoup.find_all('a', class_="", href=True)

	knots = {}

	# Create a list of found knots with de-duplication
	for a in aList:
		if( "/index.php" in a['href'] ):
			# Get the core name of the knot
			slind = a['href'].index('/')
			core_knot = a['href'][:slind]
		
			# Add only new knots. If not new, add name to names
			if( core_knot not in knots.keys() ):
				new_knot = Knot(core_knot, a.get_text(), \
								core_knot+"/index.php")
				knots[core_knot] = new_knot
			else:
				knots[core_knot].addName(a.get_text())

	# Looked at the website, realised this whole project was pointless as
	# there is not a parent/child structure to knots. Therefore, I can't
	# make a heirachy/family tree for knots ranging from less to more
	# complex. Oh well. So much for that.

	random_knot = knots[list(knots.keys())[r.randint(0, len(knots.keys())-1)]]

	print(random_knot.names[0], ": ", baseURL+random_knot.url, sep='')


class Knot:
	
	def __init__(self, core, name, url):
		self.core = core
		self.names = [name]
		self.url = url

	# Add alternate names to a knot
	def addName(self, new_name):
		# Handle adding lists of names
		if( type(new_name) == list ):
			self.names += new_name
		else:
			self.names += [new_name]

	def __repr__(self):
		return "("+self.core+", "+str(self.names)+")"


if __name__ == "__main__":
	main()
